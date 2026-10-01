# Airflow orchestration

The `claims_portfolio` DAG demonstrates a batch ELT control flow:

1. Generate deterministic synthetic source files.
2. Load raw files to Snowflake with an idempotent transaction.
3. Run dbt models and tests with `--fail-fast`.
4. Check source freshness.
5. Emit a local success notification.

Start it with `docker compose up --build`. Airflow standalone prints its local
admin credentials during startup; open `http://localhost:8080`. Snowflake
values come from `.env`, which is ignored by Git.

## Failure drills

Use these drills to practice diagnosis rather than memorizing the happy path.

### Failed load and retry

Trigger the DAG with configuration `{"fail_load": "true"}`. The loader exits
before connecting, Airflow records the exception, and retries twice. Inspect
the task log, then rerun with `false`.

### Stale source

Temporarily set the source freshness warning threshold in
`dbt_claims/models/staging/sources.yml` below the age of the loaded data.
Run `dbt source freshness`, inspect the failing source, restore the threshold,
and regenerate/load the source.

### Late-arriving status event

Add a status-history row whose event timestamp predates the latest watermark
but whose ingestion timestamp is current. The incremental model uses a
lookback window so the claim is recomputed. Explain why a strict maximum-event
timestamp watermark would silently miss this correction.

### Backfill

The DAG has `catchup=False` to avoid accidental historical runs. For a bounded
backfill, use Airflow's CLI with explicit start and end dates after confirming
the loader and dbt models are idempotent. Never start an unbounded backfill on
a paid Snowflake warehouse.

## Production differences

This is a local portfolio deployment using Airflow's SequentialExecutor. A
production setup would use a managed metadata database, remote logs, a secrets
backend, alert routing, role-separated service identities, parallel workers,
and deployment promotion between environments.
