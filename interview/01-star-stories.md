# Eight Concise STAR Stories

These are speaking outlines, not scripts to memorize. Each stays within the Candidate Evidence Bank.

## 1. Platform proposal: on-prem PostgreSQL 17

**Situation:** Manufacturing reporting depended on legacy SAP/MII queries, Excel, scripted emails, and manual reports, while the team needed a governed analytics platform.

**Task:** Propose a practical platform and a low-risk path to production.

**Action:** I proposed on-prem PostgreSQL 17 with dbt and a sandbox-to-development-to-production progression. I joined the DBA sizing session and organized the dbt layers from staging through marts, with tests and controlled TEST-before-PROD promotion.

**Result:** The platform cut over to production in mid-2026, and the Yields dashboard switched to PostgreSQL in August 2026. It now supports governed definitions and modernized Tableau/Power BI reporting.

**Boundary:** The evidence verifies the proposal, planning, sizing, cutover, and dashboard migration; it does not assign every infrastructure task to me.

## 2. Metric conflict: one governed yield definition

**Situation:** The SAP BI tool did not make voids or zero yields clear, and different audiences needed yield at different operational points. The same question produced different numbers.

**Task:** Help production, quality, and engineering reach definitions they could trust.

**Action:** I used the actual process and expected output as the discovery anchors, worked with those groups on the rules, and encoded Starts, Outputs, Voids, Scrap, and Yield once in the governed data layer. I validated current numbers before switching.

**Result:** Those measures are now defined once and reused across reporting.

**Boundary:** Do not claim sole authorship; the definitions were agreed with production, quality, and engineering.

## 3. Legacy reconciliation bug

**Situation:** During a weekly-yield cutover, the data lake and legacy SAP BI output disagreed.

**Task:** Determine whether the new logic or the trusted legacy output was wrong without disrupting users.

**Action:** I performed order-level variance analysis and used parallel verification with the stakeholder. The investigation followed differences to their calculation source instead of assuming the legacy number was correct.

**Result:** The mismatch was traced to a legacy calculation bug on July 20, 2026, supporting the controlled cutover. In related validation, I hand-calculated metrics for 10 sampled LotIDs to confirm SQL and Tableau agreed.

**Boundary:** Keep the sampled-Lot validation distinct from the July cutover unless asked about the broader reconciliation method.

## 4. Query tuning and database health

**Situation:** A PostgreSQL workload had a slowest query around 114 seconds and unnecessary storage use.

**Task:** Improve response time while protecting correctness and database health.

**Action:** I investigated execution and index behavior, tuned the slow query, and identified duplicate indexes. I also corrected a configuration defect that was forcing full rebuilds instead of incremental processing.

**Result:** The slowest query fell to about 19 seconds, roughly 6 GB was reclaimed, and incremental behavior was restored.

**Boundary:** The bank does not record the exact SQL rewrite, query plan, or index names; do not invent them.

## 5. Failed-load monitoring and early detection

**Situation:** Load problems had sometimes been discovered weeks later, increasing the cost of diagnosis and reducing trust.

**Task:** Shorten detection time and make pipeline health visible.

**Action:** I established next-morning load checks, ported two legacy quality checks, monitored build duration and database growth, and used build alerts. I also helped ensure Tableau refresh ran after each database build.

**Result:** Load health was checked the next morning rather than weeks later, with build and growth trends visible. Database tracking showed about 3.5 years of storage headroom.

**Boundary:** This is a monitoring-improvement story. The bank does not document one specific failed load, its root cause, or an exact mean-time-to-detect metric.

## 6. Technical leadership of five contractors

**Situation:** At the IRS, five contractor developers performed the development work across my two-year tenure.

**Task:** Keep delivery aligned and maintain technical quality without being their formal people manager.

**Action:** As technical lead, I directed work, kept the team on task, and ran quality control. The environment included dev/test/prod practices, an internal R package standardizing authentication and administration across seven applications, and shared PostgreSQL and SMTP components.

**Result:** The broader program delivered 13 automations associated with more than $12 million in savings.

**Boundary:** Say “technical lead and overseer,” not formal manager. Do not attribute all 13 automations or all savings solely to the five-person team without further evidence.

## 7. Stakeholder pushback: challenge a trusted metric

**Situation:** A global OEE dashboard showed quality at 100% and collapsed all AutoCaster equipment into one unit—results that did not match the process grain.

**Task:** Raise the issue constructively despite the dashboard’s apparent authority.

**Action:** I challenged the metric and grain using process knowledge and expected output, then asked for corrected figures to be validated rather than accepting the display at face value.

**Result:** Corrected quality figures were produced and verified; the aggregation defect was explicitly surfaced.

**Boundary:** The bank verifies that I raised these defects and verified corrected figures. It does not record a heated disagreement, who pushed back, or whether the AutoCaster defect was subsequently fixed. Describe this as evidence-based challenge, not interpersonal conflict.

## 8. MES hypercare and production incident response

**Situation:** An MES rollout entered Phase I hypercare with about 80 production user accounts; production support also included daily triage and a log monitor running every 15 minutes.

**Task:** Support stabilization and investigate operational data issues in a regulated manufacturing setting.

**Action:** I served on the MES core team, supported hypercare, used frequent log monitoring and triage, and investigated production symptoms. One verified example was diagnosing scrap quantity not posting on specific MES operations.

**Result:** The posting issue was diagnosed, and the monitoring/triage practices supported post-implementation stabilization.

**Boundary:** The bank does not document the root cause, resolution, outage duration, severity, or my command role in a named incident. Do not invent an incident timeline or claim formal incident-command ownership.
