# Mock Interview 1: Technical Platform and Modeling

## Format

45 minutes. Answer aloud first, then compare against the rubric. A strong answer is accurate, structured, and explicit about ownership.

## Question 1: Design the manufacturing analytics platform you proposed

**Prompt:** “Walk me through the architecture, why you chose it, and how you reduced migration risk.”

**Model answer:** “The existing environment relied on manual SAP/MII queries, Excel, scripted email, and manual reports. I proposed on-prem PostgreSQL 17 with dbt because it fit the site context and gave us a governed transformation layer. I structured transformations from incremental staging through intermediate, domain, reporting compatibility views, and marts. The rollout path was sandbox, development, then production, with DBA sizing, tests on every dbt build, and TEST-before-PROD promotion. We cut over in mid-2026, and the Yields dashboard moved to PostgreSQL in August. I would distinguish my platform proposal and data-layer work from infrastructure tasks owned by others.”

**Rubric (0–3):**

- **3:** Covers problem, architecture, layered dbt design, controlled rollout, result, and ownership boundary.
- **2:** Technically sound but misses validation, migration risk, or result.
- **1:** Lists tools without explaining decisions.
- **0:** Invents cloud scale, sole ownership, or unsupported performance claims.

## Question 2: How do you establish trusted metrics?

**Model answer:** “Yield meant different things at different operational points, and the legacy tool did not make voids or zero yields clear. I started with the process as it actually ran and a known-correct output. Production, quality, and engineering agreed the rules; then we encoded Starts, Outputs, Voids, Scrap, and Yield once in the governed layer and validated current numbers before switching. The goal was not to win a definition argument but to make grain, exclusions, and intended use explicit.”

**Rubric:** Strong answers include cross-functional definition, grain, tested implementation, reconciliation, and controlled cutover. Deduct for claiming sole authorship.

## Question 3: PostgreSQL or Snowflake?

**Model answer with honest boundary:** “My production depth is PostgreSQL and Aurora; I have not used Snowflake in production. PostgreSQL gave us control in the on-prem environment, but it required active sizing, indexing, incremental strategy, and storage monitoring. Snowflake would change the operating model through separated compute and storage and managed scaling, with consumption and workload controls becoming central. I would choose based on deployment constraints, concurrency, elasticity, governance, team skills, and total cost—not brand preference.”

**Rubric:** Strong answers make a workload-based comparison and state the Snowflake boundary immediately. Reject answers that imply Snowflake hands-on experience.

## Question 4: dbt Core or dbt Cloud?

**Model answer with honest boundary:** “I run dbt Core through a wrapper script, with tests on each build and TEST-before-PROD promotion. I have not used dbt Cloud. Core provides the transformation semantics; our team supplies orchestration and environment controls. Cloud can provide managed jobs and development workflows, but I would need hands-on time with its current environment, permission, and metadata features. My transferable depth is model layering, incremental processing, grain tests, documentation, and promotion discipline.”

**Rubric:** Full credit requires separating dbt semantics from orchestration and avoiding unsupported exposures, macros, or Cloud claims.

## Question 5: How would you move from Alteryx scheduling to Airflow?

**Model answer with honest boundary:** “I have used Alteryx Server, Windows Task Scheduler, cron, and dbt build monitoring, but not Airflow in production. I would first inventory workflows, dependencies, schedules, credentials, data contracts, retry safety, and backfill requirements. I would make tasks idempotent, migrate a low-risk vertical slice, compare outputs in parallel, add alerts and runbooks, then expand. I would not simply translate each visual step into a DAG without simplifying the underlying workflow.”

**Rubric:** Look for inventory, dependency design, idempotency, parallel validation, observability, and an explicit Airflow boundary.

## Question 6: What would you ask us?

Good questions:

- “Which layer owns business definitions, and how are definition changes approved?”
- “What are the current failure-detection and recovery targets?”
- “Where does transformation logic live today, and what is driving the desired platform change?”
- “How do you measure platform value beyond job completion?”
