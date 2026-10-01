# ADR 0001: Use a batch-first portfolio architecture

## Status

Accepted

## Context

Claims status, reserve, and payment records can arrive late or be corrected.
The portfolio must demonstrate Snowflake, dbt, Airflow, testing, retries, and
cost awareness without pretending that a small synthetic workload requires
streaming infrastructure.

## Decision

Use daily file ingestion into Snowflake raw tables, Airflow for orchestration,
and dbt incremental models with a bounded lookback for late-arriving records.
Keep Kafka as a separate literacy lab rather than inserting it into the main
pipeline.

## Consequences

- The control flow and recovery behavior remain easy to inspect.
- Auto-suspending an X-Small warehouse limits trial-account cost.
- Recent corrections are reprocessed, trading a small amount of compute for
  safer incremental behavior.
- This design does not provide real-time claim updates. If a measured business
  requirement demanded seconds-level latency, an event-driven design would be
  reconsidered.
