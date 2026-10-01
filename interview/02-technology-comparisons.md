# Technology and Role Comparisons

Each comparison distinguishes direct experience from interview-level understanding.

## PostgreSQL vs. Snowflake

**PostgreSQL:** General-purpose relational database with strong transactional and analytical SQL capabilities. It can serve operational applications and moderate analytical workloads, but teams manage sizing, indexing, vacuuming, storage, and workload contention.

**Snowflake:** Cloud analytical warehouse with separated compute and storage, elastic warehouses, consumption pricing, and managed infrastructure. It is designed primarily for analytical concurrency rather than OLTP.

**Verified experience:** PostgreSQL 17 on premises, Aurora PostgreSQL, query tuning from ~114s to ~19s, duplicate-index cleanup reclaiming ~6 GB, incremental dbt builds, and database-growth monitoring.

**Honest answer:** “I have not used Snowflake in production. My production depth is PostgreSQL and Aurora. The transferable skills are dimensional modeling, SQL tuning, incremental processing, testing, workload governance, and cost/capacity awareness. In Snowflake I would need to learn warehouse sizing, clustering behavior, Snowpipe, and account-specific cost controls.”

## Schedulers/Alteryx vs. Airflow

**Schedulers and Alteryx:** Windows Task Scheduler and cron trigger commands at set times; Alteryx Server schedules visual workflows. They are effective for bounded workflows but can make cross-pipeline dependencies, code review, backfills, and observability less explicit.

**Airflow:** Code-defined DAG orchestration with task dependencies, retries, scheduling, backfills, metadata, and operational views. It orchestrates work; it is not the transformation engine itself.

**Verified experience:** Windows Task Scheduler, cron, Alteryx Designer/Server, dbt build monitoring, scheduler-based reporting, and a planned config-driven runner replacing Alteryx.

**Honest answer:** “I have not run Airflow in production. I have operated scheduled workflows and monitored dbt builds, so dependencies, idempotency, retries, alerts, and backfills are familiar concerns. I would not claim Airflow DAG authorship.”

## dbt Core vs. dbt Cloud

**dbt Core:** Open-source CLI for compiling, running, testing, and documenting SQL transformations. The team supplies scheduling, environment management, CI, secrets, and operational interfaces.

**dbt Cloud:** Managed dbt development and orchestration with hosted IDE, jobs, environment controls, metadata features, and integrated workflows. Exact features depend on plan and release.

**Verified experience:** dbt with staging → intermediate → domain → reporting → mart layers; incremental watermark models; tests on every build; schema documentation; seeds; TEST-before-PROD promotion; wrapper-script execution.

**Honest answer:** “My production work is dbt Core through a wrapper script, not dbt Cloud. I understand the transformation semantics, tests, lineage-oriented layering, and promotion controls; I would need hands-on time with Cloud jobs, environments, permissions, and its current metadata features. I also have no verified use of dbt exposures or macros.”

## Batch vs. Kafka

**Batch:** Processes bounded data on a schedule or trigger. It is simpler to operate and replay when minute- or hour-level latency is acceptable.

**Kafka:** Distributed event streaming built around ordered partition logs, consumer groups, retention, and replay. It supports low-latency event-driven systems but requires schema, partitioning, delivery-semantics, lag, and operational decisions.

**Verified experience:** Batch/scheduled ETL, DMS/CDC, data ingested twice per hour, dbt incremental builds, Tableau refresh triggering, and 15-minute MES log monitoring.

**Honest answer:** “I have not used Kafka. My closest experience is CDC and frequent incremental ingestion, but I would not equate that with operating Kafka. I can discuss event keys, ordering, idempotent consumers, replay, schema evolution, and lag as design concerns, not as production claims.”

## S3/Iceberg vs. Delta Lake

**S3 + Iceberg:** S3 supplies object storage; Iceberg adds table metadata, schema evolution, partition evolution, snapshots, and transactional table semantics across compatible engines.

**Delta Lake:** Another lakehouse table format, closely associated with the Databricks ecosystem, with transaction logs, schema enforcement/evolution, and time travel.

**Verified experience:** AutoCos flow using DMS/CDC → S3 → Iceberg → SageMaker on the global side; about 41 GB/~11,000 images moved to S3; S3 File Gateway provisioned. The evidence does not define Michael's ownership of every global-side component.

**Honest answer:** “I have worked around an S3/Iceberg architecture, including S3 transfer and File Gateway work, but I have no Delta Lake or Databricks production experience. I would compare both on engine compatibility, catalog integration, concurrency, governance, maintenance, and the organization’s existing platform.”

## Git vs. CI/CD

**Git:** Version control: commits, branches, diffs, merge history, and collaboration around source.

**CI/CD:** Automated integration and delivery controls that build, test, package, and promote changes. Git often triggers CI/CD, but using Git does not itself prove pipeline experience.

**Verified experience:** Enterprise GitHub, versioned work, tests on each dbt build, TEST-before-PROD promotion, dev/test/prod environments at the IRS, and controlled work packets/runbooks reviewed and executed by hand.

**Honest answer:** “I use Git and controlled promotion practices, but I have no verified hands-on GitHub Actions or Azure DevOps Pipelines experience. My current controls include automated dbt tests and manual reviewed promotion; I would not label that a fully automated CI/CD pipeline.”

## Technical lead vs. formal people manager

**Technical lead:** Directs technical work, reviews quality, sets standards, resolves design issues, mentors, and coordinates delivery—often without authority over compensation, performance ratings, or hiring.

**Formal people manager:** Owns recurring 1:1s, performance management, hiring, compensation input, career development, staffing, and organizational accountability.

**Verified experience:** Technical lead over five IRS contractors for two years; Army leadership of about 30 combat medics, a doctor, and a physician assistant; Math Department Chair; Test Prep Coordinator for 30+ teachers; Head TA.

**Honest answer:** “I have substantial leadership experience and two years directing five contractor developers with quality control, but I have not formally managed a data or BI team for three to five years. I would bring a tested leadership foundation while adopting the company’s people-management processes.”
