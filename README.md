# Claims Data Platform Portfolio

[![CI](https://github.com/mkuehn10/claims-data-platform-portfolio/actions/workflows/ci.yml/badge.svg)](https://github.com/mkuehn10/claims-data-platform-portfolio/actions/workflows/ci.yml)

A deliberately small, reproducible data-engineering portfolio built with
synthetic property-and-casualty claims data. It demonstrates Snowflake, dbt,
Airflow, data-quality testing, incremental processing, CI, and operational
documentation without presenting lab work as production experience.

## Architecture

Deterministic Python generation → CSV landing files → Snowflake `RAW` tables →
dbt staging/core/mart models. Airflow controls ordering, retries, and freshness;
GitHub Actions checks Python, dbt parsing, and secrets. See
[`docs/architecture.md`](docs/architecture.md).

## Quick start without cloud credentials

Prerequisites: Python 3.12 and
[uv](https://docs.astral.sh/uv/).

```powershell
uv sync
uv run generate-claims-data --output-dir data/synthetic --seed 6644
uv run ruff check .
uv run pytest
```

The generator creates only synthetic policies, first-notice-of-loss claims,
reserve changes, payments, and status history. The tests check deterministic
output, key relationships, lifecycle ordering, positive payments, and closed
claim reconciliation.

## Snowflake and dbt

1. Create a Snowflake trial/development account.
2. Run `docs/sql/bootstrap_snowflake.sql` with an administrative role.
3. Copy `.env.example` to `.env` and fill values locally. Never commit it.
4. Generate source files and load them:

```powershell
uv run generate-claims-data --output-dir data/synthetic --seed 6644
uv run load-claims-snowflake --input-dir data/synthetic
uv run dbt build --project-dir dbt_claims --profiles-dir dbt_profiles
uv run dbt source freshness --project-dir dbt_claims --profiles-dir dbt_profiles
```

The project includes staged, intermediate, dimensional, fact, and mart models;
an incremental transaction fact with a 14-day late-arrival lookback; an SCD2
claim-status snapshot; source freshness; relationships and accepted-values
tests; and singular business-rule tests.

Use an X-Small warehouse with auto-suspend. Record query duration and bytes
scanned before changing warehouse size or clustering.

## Airflow

Copy `.env.example` to `.env`, then run:

```powershell
docker compose up --build
```

Open `http://localhost:8080` and trigger `claims_portfolio`. Airflow standalone
prints local credentials at startup. Failure drills and production differences
are documented in [`airflow/README.md`](airflow/README.md).

## Secondary labs and interview practice

- [`labs/`](labs/) contains bounded Spark/Delta, Terraform, and Kafka exercises.
- [`interview/`](interview/) contains verified STAR stories, comparisons,
  domain bridges, a prospective management model, and mock interviews.
- [`docs/runbook.md`](docs/runbook.md) covers validation and failure triage.
- [`docs/snowflake-airflow-notes.md`](docs/snowflake-airflow-notes.md) is a
  concise interview-oriented mental model.

## Honest scope

This repository shows hands-on portfolio work, not employer production
experience with Snowflake, Airflow, Databricks, Spark, Terraform, or Kafka. It
uses synthetic data, a local Airflow executor, and intentionally small
workloads. The documentation identifies what would change for production.

## License

MIT
