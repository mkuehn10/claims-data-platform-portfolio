"""Orchestrate synthetic claims generation, loading, transformation, and tests."""

from __future__ import annotations

from datetime import datetime, timedelta

from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from airflow import DAG

PROJECT_DIR = "/opt/project"
DBT_DIR = f"{PROJECT_DIR}/dbt_claims"
PROFILES_DIR = f"{PROJECT_DIR}/dbt_profiles"


def report_success(**context: object) -> None:
    """Emit a local success notification without external credentials."""
    run_id = context["run_id"]
    print(f"Claims portfolio pipeline completed successfully: {run_id}")


with DAG(
    dag_id="claims_portfolio",
    description="Synthetic claims ELT demonstrating retries, tests, and backfills",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    max_active_runs=1,
    default_args={
        "owner": "portfolio",
        "retries": 2,
        "retry_delay": timedelta(minutes=1),
        "execution_timeout": timedelta(minutes=20),
    },
    tags=["portfolio", "snowflake", "dbt"],
) as dag:
    generate_claims = BashOperator(
        task_id="generate_claims",
        bash_command=(
            f"cd {PROJECT_DIR} && "
            "generate-claims-data "
            "--output-dir data/synthetic --seed 6644"
        ),
    )

    load_raw = BashOperator(
        task_id="load_raw_to_snowflake",
        bash_command=(
            f"cd {PROJECT_DIR} && load-claims-snowflake --input-dir data/synthetic"
        ),
        env={"FAIL_LOAD": "{{ params.fail_load | default('false') }}"},
        append_env=True,
    )

    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command=(
            f"cd {DBT_DIR} && "
            f"dbt build --profiles-dir {PROFILES_DIR} "
            "--target dev --fail-fast"
        ),
    )

    verify_freshness = BashOperator(
        task_id="verify_source_freshness",
        bash_command=(
            f"cd {DBT_DIR} && "
            f"dbt source freshness --profiles-dir {PROFILES_DIR} --target dev"
        ),
    )

    notify_success = PythonOperator(
        task_id="notify_success",
        python_callable=report_success,
    )

    generate_claims >> load_raw >> dbt_build >> verify_freshness >> notify_success
