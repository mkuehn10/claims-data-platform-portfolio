from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import pytest

from claims_portfolio.generator import generate_dataset


def read_rows(directory: Path, table: str) -> list[dict[str, str]]:
    with (directory / f"{table}.csv").open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_generation_is_deterministic(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"

    first_counts = generate_dataset(first, seed=42, policy_count=50)
    second_counts = generate_dataset(second, seed=42, policy_count=50)

    assert first_counts == second_counts
    for filename in first.iterdir():
        assert filename.read_bytes() == (second / filename.name).read_bytes()


def test_relations_and_lifecycle_invariants(tmp_path: Path) -> None:
    generate_dataset(tmp_path, seed=6644, policy_count=100)
    policies = read_rows(tmp_path, "policies")
    claims = read_rows(tmp_path, "claims")
    reserves = read_rows(tmp_path, "reserve_transactions")
    payments = read_rows(tmp_path, "payments")
    statuses = read_rows(tmp_path, "claim_status_history")

    policy_ids = {row["policy_id"] for row in policies}
    claim_ids = {row["claim_id"] for row in claims}
    assert len(policy_ids) == len(policies)
    assert len(claim_ids) == len(claims)
    assert all(row["policy_id"] in policy_ids for row in claims)
    assert all(row["claim_id"] in claim_ids for row in reserves + payments + statuses)
    assert all(float(row["payment_amount"]) > 0 for row in payments)
    assert all(row["effective_date"] < row["expiration_date"] for row in policies)

    events_by_claim: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in statuses:
        events_by_claim[row["claim_id"]].append(row)
    for claim in claims:
        events = sorted(
            events_by_claim[claim["claim_id"]],
            key=lambda row: row["status_effective_at"],
        )
        assert [event["status"] for event in events[:2]] == ["REPORTED", "OPEN"]
        assert events[-1]["status"] == claim["current_status"]


def test_closed_claim_reserve_equals_paid(tmp_path: Path) -> None:
    generate_dataset(tmp_path, policy_count=125)
    claims = read_rows(tmp_path, "claims")
    reserves = read_rows(tmp_path, "reserve_transactions")
    payments = read_rows(tmp_path, "payments")
    reserve_totals: dict[str, float] = defaultdict(float)
    paid_totals: dict[str, float] = defaultdict(float)
    for row in reserves:
        reserve_totals[row["claim_id"]] += float(row["reserve_change_amount"])
    for row in payments:
        paid_totals[row["claim_id"]] += float(row["payment_amount"])
    for claim in claims:
        if claim["current_status"] == "CLOSED":
            assert reserve_totals[claim["claim_id"]] == pytest.approx(
                paid_totals[claim["claim_id"]],
                abs=0.02,
            )


def test_rejects_non_positive_policy_count(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="positive"):
        generate_dataset(tmp_path, policy_count=0)
