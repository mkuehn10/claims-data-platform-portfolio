# Mock Interview 2: Technical Reliability and Incident Reasoning

## Format

45 minutes. Favor diagnosis, evidence, and safe recovery over tool-name fluency.

## Question 1: A trusted legacy report disagrees with your new model. What do you do?

**Model answer:** “I do not assume either side is correct. I declare the grain and definitions, identify a small set of differing records, and compare inputs and rule application at order level. For our weekly yield cutover, I used order-level variance analysis and parallel verification with the stakeholder. The mismatch was ultimately traced to a legacy calculation bug. In related validation, I hand-calculated 10 sampled LotIDs to confirm SQL and Tableau agreed. I would keep both outputs visible until the discrepancy is explained and accepted.”

**Rubric (0–3):**

- **3:** Defines grain, isolates records, traces rules, validates independently, and uses parallel cutover.
- **2:** Reconciles totals but lacks record-level method or cutover control.
- **1:** Assumes the new or old system is authoritative.
- **0:** Changes logic until totals happen to match.

## Question 2: Describe a performance improvement

**Model answer:** “Our slowest query was about 114 seconds. I investigated query and index behavior, tuned it to about 19 seconds, identified duplicate indexes that allowed us to reclaim roughly 6 GB, and corrected a configuration defect that was forcing full rather than incremental rebuilds. I would not invent the exact query-plan steps because they are not in my prepared evidence, but the lesson is to treat runtime, storage, and pipeline configuration as one system.”

**Rubric:** Full credit requires exact verified metrics, systems thinking, and no fabricated SQL or plan details.

## Question 3: How do you monitor failed loads?

**Model answer:** “The important change was moving detection from potentially weeks later to next-morning checks. We ported two legacy quality checks and monitored build duration and database growth, with build alerts and downstream refresh coordination. That gave us earlier evidence and about 3.5 years of projected storage headroom. I can describe the monitoring improvement; I do not have a verified single failed-load incident or mean-time-to-detect number to claim.”

**Rubric:** Strong answers cover freshness, validity, duration, growth, downstream effects, alert ownership, and the evidence boundary.

## Question 4: When would you choose batch versus Kafka?

**Model answer with honest boundary:** “I have not used Kafka. My production experience is scheduled and incremental processing, DMS/CDC, twice-hourly ingestion, and frequent monitoring. If the business can tolerate bounded latency and values simpler replay and operations, batch may be the better choice. Kafka becomes attractive for low-latency event distribution and multiple independent consumers, but it adds partition-key, ordering, schema, lag, replay, and delivery-semantics decisions. I would first quantify the latency requirement rather than treating streaming as inherently better.”

**Rubric:** Full credit requires a business-latency decision, operational tradeoffs, and explicit non-experience.

## Question 5: Compare S3/Iceberg and Delta Lake

**Model answer with honest boundary:** “I worked around a global flow using DMS/CDC to S3 and Iceberg, then SageMaker, and I provisioned S3 File Gateway as part of the broader AutoCos work. I have no Delta Lake or Databricks production experience, and I would not claim ownership of every global-side component. Architecturally, both Iceberg and Delta add transactional table semantics to object storage. I would evaluate engine and catalog compatibility, governance, schema and partition evolution, concurrency, maintenance, and the existing platform ecosystem.”

**Rubric:** Strong answers separate object storage from table format, avoid overstating ownership, and state the Delta boundary.

## Question 6: Tell me about an MES incident

**Model answer with honest boundary:** “I supported the MES core team and Phase I hypercare for roughly 80 production user accounts. We had a 15-minute log monitor and daily triage, and I diagnosed scrap quantity not posting on specific MES operations. The evidence I have prepared does not include the root cause, resolution, severity, or outage duration, so I would not manufacture an incident timeline. What I can demonstrate is production triage, evidence gathering, and regulated-system support.”

**Rubric:** Full credit rewards precision and restraint. Do not reward invented severity, root cause, remediation, or command role.
