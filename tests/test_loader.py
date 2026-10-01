from __future__ import annotations

from pathlib import Path

import pytest

from claims_portfolio.load_snowflake import (
    _connection_parameters,
    _read_csv,
    load_directory,
)


def test_connection_parameters_report_all_missing_values(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for name in (
        "SNOWFLAKE_ACCOUNT",
        "SNOWFLAKE_USER",
        "SNOWFLAKE_PASSWORD",
        "SNOWFLAKE_DATABASE",
        "SNOWFLAKE_WAREHOUSE",
    ):
        monkeypatch.delenv(name, raising=False)

    with pytest.raises(RuntimeError, match="SNOWFLAKE_ACCOUNT"):
        _connection_parameters()


def test_read_csv_rejects_empty_file(tmp_path: Path) -> None:
    empty = tmp_path / "empty.csv"
    empty.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="no header"):
        _read_csv(empty)


def test_failure_drill_stops_before_read_or_connect(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("FAIL_LOAD", "true")

    with pytest.raises(RuntimeError, match="Intentional failure drill"):
        load_directory(tmp_path)
