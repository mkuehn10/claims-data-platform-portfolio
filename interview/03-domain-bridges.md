# Honest Insurance and Healthcare Domain Bridges

## Property and casualty insurance

**Direct boundary:** I have no production property-and-casualty claims experience.

**Verified bridges:**

- Exception and aging workflows in FDA-regulated manufacturing: on-hold batches, aged WIP, and edge-template exceptions.
- Edge-template compliance screened 230K+ historical confirmations, reduced routine QA review from hundreds per week to fewer than five per day, and sent exceptions three times daily.
- IRS work involved regulated financial data and 13 automations associated with more than $12 million in savings.
- Shared metric governance: Starts, Outputs, Voids, Scrap, and Yield were defined once after cross-functional agreement.

**Model answer:** “I have not worked with P&C policy or claims data, so I would not pretend that manufacturing exceptions are claims. The bridge is in engineering regulated case-lifecycle data: defining state and aging rules, routing exceptions, preserving traceability, reconciling outputs, and giving reviewers a manageable queue. I would pair that engineering experience with deliberate learning of policy, coverage, reserve, loss, and claims-handling concepts.”

**Do not claim:** claims adjudication, loss reserving, policy administration, ACORD data, Guidewire, Duck Creek, or insurance regulatory expertise.

## Healthcare claims and payment integrity

**Direct boundary:** I have no production experience with 837/835 transactions, UB-04, DRGs, provider contracts, coding edits, or payment-integrity adjudication.

**Verified bridges:**

- FDA-regulated medical-device manufacturing data across production, quality, inspection, sterilization, and MES processes.
- On-hold-batch reporting joined SAP quality notifications, confirmations, sterilization data, and Teamcenter records to support QA release.
- Rule-based exception workflow: every edge-template record was classified against an expected rule and only exceptions reached reviewers.
- Reconciliation at order and sampled-lot level, including hand calculation of 10 LotIDs and discovery of a legacy calculation bug.
- Army medical leadership and medical training experience are healthcare-adjacent leadership, not claims-domain experience.

**Model answer:** “I have not handled healthcare claims or payment-integrity data. My closest experience is regulated medical-device and federal data, where correctness, traceability, controlled validation, and exception review matter. I have built rule-driven exception feeds and reconciled legacy calculations, but I would need domain partnership to learn claim forms, code sets, contractual rules, and clinical context.”

**Do not claim:** HIPAA expertise, payer/provider operations, clinical analytics, claims adjudication, fraud/waste/abuse models, or medical coding expertise.

## A credible first-90-day domain approach

This is a proposed approach, not past experience:

1. Learn the lifecycle and vocabulary from domain owners before proposing a data model.
2. Trace several real records end to end, including reversals, corrections, late arrivals, and denials/exceptions.
3. Write down grain, state transitions, authoritative sources, and reconciliation totals.
4. Encode rules in tested transformations and validate against current operational numbers.
5. Run old and new outputs in parallel before cutover.

That approach mirrors the verified discovery and reconciliation method used in manufacturing without claiming the domains are identical.
