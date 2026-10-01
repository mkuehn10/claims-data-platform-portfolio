"""Load generated claims CSVs into Snowflake raw tables."""

from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path

REQUIRED_ENV = (
    "SNOWFLAKE_ACCOUNT",
    "SNOWFLAKE_USER",
    "SNOWFLAKE_PASSWORD",
    "SNOWFLAKE_DATABASE",
    "SNOWFLAKE_WAREHOUSE",
)
TABLES = (
    "policies",
    "claims",
    "reserve_transactions",
    "payments",
    "claim_status_history",
)


def _connection_parameters() -> dict[str, str]:
    missing = [name for name in REQUIRED_ENV if not os.getenv(name)]
    if missing:
        names = ", ".join(missing)
        raise RuntimeError(f"Missing required environment variables: {names}")
    return {
        "account": os.environ["SNOWFLAKE_ACCOUNT"],
        "user": os.environ["SNOWFLAKE_USER"],
        "password": os.environ["SNOWFLAKE_PASSWORD"],
        "database": os.environ["SNOWFLAKE_DATABASE"],
        "warehouse": os.environ["SNOWFLAKE_WAREHOUSE"],
        "role": os.getenv("SNOWFLAKE_LOADER_ROLE", "CLAIMS_LOADER"),
        "session_parameters": {"QUERY_TAG": "claims_portfolio_loader"},
    }


def _read_csv(path: Path) -> tuple[list[str], list[tuple[str, ...]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"{path} has no header")
        rows = [tuple(row[column] for column in reader.fieldnames) for row in reader]
    if not rows:
        raise ValueError(f"{path} has no data rows")
    return reader.fieldnames, rows


def _quoted(identifier: str) -> str:
    if not identifier.replace("_", "").isalnum():
        raise ValueError(f"Unsafe identifier: {identifier}")
    return f'"{identifier.upper()}"'


def load_directory(input_dir: Path) -> dict[str, int]:
    """Replace raw table contents atomically after validating all input files."""
    if os.getenv("FAIL_LOAD", "false").lower() == "true":
        raise RuntimeError("Intentional failure drill requested by FAIL_LOAD")

    batches: dict[str, tuple[list[str], list[tuple[str, ...]]]] = {}
    for table in TABLES:
        batches[table] = _read_csv(input_dir / f"{table}.csv")

    import snowflake.connector

    connection = snowflake.connector.connect(**_connection_parameters())
    counts: dict[str, int] = {}
    try:
        cursor = connection.cursor()
        for table, (columns, _) in batches.items():
            definitions = ", ".join(f"{_quoted(column)} varchar" for column in columns)
            cursor.execute(
                f"create table if not exists RAW.{_quoted(table)} "
                f"({definitions}, _INGESTED_AT timestamp_tz)"
            )
            cursor.execute(
                f"alter table RAW.{_quoted(table)} "
                "add column if not exists _INGESTED_AT timestamp_tz"
            )

        connection.autocommit(False)
        cursor.execute("begin")
        for table in reversed(TABLES):
            cursor.execute(f"delete from RAW.{_quoted(table)}")
        for table, (columns, rows) in batches.items():
            names = ", ".join(_quoted(column) for column in columns)
            names = f"{names}, _INGESTED_AT"
            placeholders = ", ".join(["%s"] * len(columns))
            cursor.executemany(
                f"insert into RAW.{_quoted(table)} ({names}) "
                f"select {placeholders}, current_timestamp()",
                rows,
            )
            counts[table] = len(rows)
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
    return counts


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, default=Path("data/synthetic"))
    args = parser.parse_args()
    counts = load_directory(args.input_dir)
    for table, count in counts.items():
        print(f"{table}: {count}")


if __name__ == "__main__":
    main()
