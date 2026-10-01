"""Generate deterministic, relational P&C claims lifecycle CSV files."""

from __future__ import annotations

import argparse
import csv
import random
from collections.abc import Iterable
from datetime import UTC, date, datetime, time, timedelta
from pathlib import Path
from typing import Any

LINE_CONFIG = {
    "AUTO": {
        "states": ("FL", "GA", "NC", "SC"),
        "coverage": ("BI", "PD", "COLLISION", "COMPREHENSIVE"),
        "premium": (720, 2400),
        "limit": (25_000, 300_000),
    },
    "HOME": {
        "states": ("FL", "GA", "NC", "SC"),
        "coverage": ("DWELLING", "CONTENTS", "LIABILITY", "ALE"),
        "premium": (900, 4200),
        "limit": (100_000, 750_000),
    },
}
CAUSES = {
    "AUTO": ("collision", "weather", "theft", "glass"),
    "HOME": ("wind", "water", "fire", "theft"),
}


def _iso(value: date | datetime) -> str:
    return value.isoformat()


def _utc(day: date, hour: int = 12) -> datetime:
    return datetime.combine(day, time(hour), tzinfo=UTC)


def _money(value: float) -> str:
    return f"{value:.2f}"


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _status_events(
    claim_id: str,
    reported: date,
    close_day: date | None,
    reopen_day: date | None,
) -> list[dict[str, str]]:
    events = [
        {
            "status_event_id": f"{claim_id}-S01",
            "claim_id": claim_id,
            "status": "REPORTED",
            "status_effective_at": _iso(_utc(reported, 9)),
            "recorded_at": _iso(_utc(reported, 10)),
        },
        {
            "status_event_id": f"{claim_id}-S02",
            "claim_id": claim_id,
            "status": "OPEN",
            "status_effective_at": _iso(_utc(reported, 11)),
            "recorded_at": _iso(_utc(reported, 11)),
        },
    ]
    if close_day is not None:
        events.append(
            {
                "status_event_id": f"{claim_id}-S03",
                "claim_id": claim_id,
                "status": "CLOSED",
                "status_effective_at": _iso(_utc(close_day)),
                "recorded_at": _iso(_utc(close_day)),
            }
        )
    if reopen_day is not None:
        events.append(
            {
                "status_event_id": f"{claim_id}-S04",
                "claim_id": claim_id,
                "status": "REOPENED",
                "status_effective_at": _iso(_utc(reopen_day)),
                # Deliberately late-arriving, but deterministically so.
                "recorded_at": _iso(_utc(reopen_day + timedelta(days=9))),
            }
        )
    return events


def generate_dataset(
    output_dir: Path,
    *,
    seed: int = 6644,
    policy_count: int = 250,
) -> dict[str, int]:
    """Generate a complete deterministic dataset and return table row counts."""
    if policy_count < 1:
        raise ValueError("policy_count must be positive")

    rng = random.Random(seed)
    policies: list[dict[str, Any]] = []
    claims: list[dict[str, Any]] = []
    reserves: list[dict[str, Any]] = []
    payments: list[dict[str, Any]] = []
    statuses: list[dict[str, Any]] = []
    base_day = date(2022, 1, 1)
    claim_sequence = 0

    for index in range(1, policy_count + 1):
        policy_id = f"POL-{index:06d}"
        line = "AUTO" if index % 3 else "HOME"
        config = LINE_CONFIG[line]
        effective = base_day + timedelta(days=rng.randrange(0, 730))
        expiration = effective + timedelta(days=365)
        state = rng.choice(config["states"])
        premium = rng.uniform(*config["premium"])
        coverage_limit = (
            rng.randrange(
                config["limit"][0] // 1000,
                config["limit"][1] // 1000 + 1,
            )
            * 1000
        )
        policies.append(
            {
                "policy_id": policy_id,
                "policy_number": f"{line}-{100000 + index}",
                "customer_id": f"CUST-{((index - 1) % 180) + 1:06d}",
                "line_of_business": line,
                "risk_state": state,
                "effective_date": _iso(effective),
                "expiration_date": _iso(expiration),
                "annual_premium": _money(premium),
                "coverage_limit": _money(coverage_limit),
                "loaded_at": _iso(_utc(effective - timedelta(days=15))),
            }
        )

        claim_total = rng.choices((0, 1, 2), weights=(46, 45, 9), k=1)[0]
        for _ in range(claim_total):
            claim_sequence += 1
            claim_id = f"CLM-{claim_sequence:07d}"
            loss_day = effective + timedelta(days=rng.randrange(1, 355))
            reported = loss_day + timedelta(days=rng.randrange(0, 8))
            claim_age = (base_day + timedelta(days=1095) - reported).days
            is_closed = claim_age > 90 and rng.random() < 0.74
            close_day = (
                reported + timedelta(days=rng.randrange(15, min(180, claim_age) + 1))
                if is_closed
                else None
            )
            is_reopened = close_day is not None and rng.random() < 0.08
            reopen_day = (
                close_day + timedelta(days=rng.randrange(7, 45))
                if is_reopened
                else None
            )
            current_status = (
                "REOPENED" if reopen_day else ("CLOSED" if close_day else "OPEN")
            )
            coverage = rng.choice(config["coverage"])
            severity = min(
                coverage_limit,
                round(rng.lognormvariate(8.5 if line == "AUTO" else 9.2, 0.85), 2),
            )
            fnol_channel = rng.choice(("AGENT", "WEB", "PHONE", "MOBILE"))
            claims.append(
                {
                    "claim_id": claim_id,
                    "claim_number": f"{loss_day.year}-{claim_sequence:07d}",
                    "policy_id": policy_id,
                    "loss_date": _iso(loss_day),
                    "reported_at": _iso(_utc(reported, 9)),
                    "fnol_channel": fnol_channel,
                    "cause_of_loss": rng.choice(CAUSES[line]),
                    "coverage_type": coverage,
                    "loss_state": state,
                    "current_status": current_status,
                    "closed_at": _iso(_utc(close_day)) if close_day else "",
                    "reopened_at": _iso(_utc(reopen_day)) if reopen_day else "",
                    "loaded_at": _iso(_utc(reported, 10)),
                }
            )
            statuses.extend(_status_events(claim_id, reported, close_day, reopen_day))

            initial_reserve = max(500.0, severity * rng.uniform(0.65, 1.15))
            reserves.append(
                {
                    "reserve_event_id": f"{claim_id}-R01",
                    "claim_id": claim_id,
                    "coverage_type": coverage,
                    "transaction_date": _iso(reported),
                    "reserve_change_amount": _money(initial_reserve),
                    "reserve_reason": "INITIAL",
                    "recorded_at": _iso(_utc(reported, 12)),
                }
            )
            if severity > initial_reserve * 1.1:
                adjustment_day = reported + timedelta(days=rng.randrange(7, 30))
                reserves.append(
                    {
                        "reserve_event_id": f"{claim_id}-R02",
                        "claim_id": claim_id,
                        "coverage_type": coverage,
                        "transaction_date": _iso(adjustment_day),
                        "reserve_change_amount": _money(severity - initial_reserve),
                        "reserve_reason": "ADJUSTMENT",
                        "recorded_at": _iso(_utc(adjustment_day)),
                    }
                )

            payment_count = rng.randrange(1, 4) if (close_day or claim_age > 30) else 0
            paid_total = 0.0
            for payment_index in range(1, payment_count + 1):
                fraction = 1 / payment_count
                amount = severity * fraction
                paid_total += amount
                payment_day = reported + timedelta(days=10 + payment_index * 12)
                payments.append(
                    {
                        "payment_id": f"{claim_id}-P{payment_index:02d}",
                        "claim_id": claim_id,
                        "payment_date": _iso(payment_day),
                        "payment_type": (
                            "INDEMNITY" if payment_index % 3 else "EXPENSE"
                        ),
                        "payee_type": rng.choice(
                            ("INSURED", "VENDOR", "CLAIMANT", "ATTORNEY")
                        ),
                        "payment_amount": _money(amount),
                        "recorded_at": _iso(_utc(payment_day)),
                    }
                )
            if close_day is not None:
                reserve_balance = initial_reserve
                if severity > initial_reserve * 1.1:
                    reserve_balance = severity
                release = paid_total - reserve_balance
                if abs(release) >= 0.01:
                    reserves.append(
                        {
                            "reserve_event_id": f"{claim_id}-R99",
                            "claim_id": claim_id,
                            "coverage_type": coverage,
                            "transaction_date": _iso(close_day),
                            "reserve_change_amount": _money(release),
                            "reserve_reason": "CLOSE_RELEASE",
                            "recorded_at": _iso(_utc(close_day)),
                        }
                    )

    tables = {
        "policies": policies,
        "claims": claims,
        "reserve_transactions": reserves,
        "payments": payments,
        "claim_status_history": statuses,
    }
    for table_name, rows in tables.items():
        _write_csv(output_dir / f"{table_name}.csv", rows)
    return {table_name: len(rows) for table_name, rows in tables.items()}


def _summary_lines(counts: dict[str, int]) -> Iterable[str]:
    for table_name, count in counts.items():
        yield f"{table_name}: {count}"


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("data/synthetic"))
    parser.add_argument("--seed", type=int, default=6644)
    parser.add_argument("--policy-count", type=int, default=250)
    args = parser.parse_args()
    counts = generate_dataset(
        args.output_dir,
        seed=args.seed,
        policy_count=args.policy_count,
    )
    print("\n".join(_summary_lines(counts)))


if __name__ == "__main__":
    main()
