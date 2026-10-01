# Snowflake and Airflow interview notes

These notes describe the portfolio implementation, not production employment
experience.

## Snowflake mental model

- **Storage and compute are separate.** Databases/schemas/tables hold data;
  virtual warehouses supply compute and can independently size, resume, and
  suspend.
- **Micro-partitions are automatic.** Pruning works when filters align with
  useful clustering metadata. Clustering keys are not ordinary indexes and
  should follow measured pruning problems, not habit.
- **Cost is credits over time.** Start with X-Small, auto-suspend quickly,
  avoid idle polling, inspect Query History, and resize only after profiling.
- **Roles grant capabilities.** Separate loading from transformation, grant
  least privilege, and avoid using ACCOUNTADMIN for application work.
- **Stages and COPY scale file loading.** This small project uses parameterized
  inserts for readability; production-sized files should use an internal or
  external stage plus `COPY INTO`, load metadata, and rejected-row handling.
- **Time Travel and zero-copy clones** help recovery and isolated testing, but
  retention consumes storage and does not replace backups or access controls.

## PostgreSQL comparison

PostgreSQL combines a database engine and compute on a server or managed
instance. It offers indexes, constraints, and transactional application
workloads. Snowflake optimizes analytical concurrency and elastic compute,
uses micro-partition metadata rather than conventional indexes, and commonly
enforces data quality in pipelines rather than physical constraints. Neither
is universally better; workload, latency, concurrency, governance, and cost
decide.

## Airflow mental model

- A DAG declares task dependencies; it should not hide all business logic in
  the scheduler.
- The scheduler creates task instances, while an executor determines where
  they run.
- Retries address transient failures. They do not fix deterministic bad data,
  non-idempotent writes, or incorrect logic.
- Catchup and backfill are different from a normal retry and can multiply
  cost. Bound date ranges and confirm idempotency first.
- XCom is control-plane metadata, not a path for large datasets.
- Sensors wait for conditions; deferrable sensors avoid occupying a worker
  slot while waiting.
- Connections and secrets belong in a secrets backend or managed connection,
  not DAG source code.

## What I can claim after running this project

“I built and tested a portfolio pipeline using Snowflake, dbt, and Airflow. I
can explain the architecture, incremental and late-arriving-data strategy,
retries, freshness checks, permissions, and cost controls. I have not operated
those tools in a production employer environment.”
