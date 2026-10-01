# Claims pipeline runbook

## Before a run

1. Confirm `.env` exists locally and is not tracked.
2. Confirm the Snowflake warehouse is X-Small with auto-suspend enabled.
3. Run `uv sync --locked`.
4. Generate and validate source data with `uv run claims-generate`.
5. Use a development schema; never point this project at employer data.

## Local quality checks

Run:

```powershell
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv run dbt parse --project-dir dbt_claims --profiles-dir dbt_profiles --no-partial-parse
```

## Airflow run

Start with `docker compose up --build`, open the Airflow UI, and trigger
`claims_portfolio`. Follow the task chain rather than rerunning the entire DAG
without reading the failed task log.

## Triage order

1. **Generation failed:** verify Python dependencies and write access to
   `data/generated`.
2. **Load failed:** verify required environment variables, account identifier,
   role grants, file schema, and Snowflake query history.
3. **dbt build failed:** identify the first failed model/test, inspect compiled
   SQL, and check source key/null/relationship assumptions.
4. **Freshness failed:** compare loaded-at timestamps with the freshness SLA;
   do not suppress the test before establishing whether ingestion is stale.
5. **Unexpected row counts:** compare raw file and raw-table counts, then test
   join grain for fan-out before rerunning.

## Recovery

The loader replaces each deterministic synthetic raw table in one transaction,
and dbt models are rebuildable. Retry only after identifying the failure. For a
late correction, retain a current ingestion timestamp so the incremental
lookback recomputes affected claims.

## Cost control

Use Query History to record bytes scanned, elapsed time, and warehouse size for
one dbt build. Suspend the warehouse after work. Do not enable multi-cluster
warehouses or leave BI tools polling the trial account.
