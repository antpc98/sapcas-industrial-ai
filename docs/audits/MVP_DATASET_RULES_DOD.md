# MVP Dataset Audit & Business Rules — Closure

## Task and planning context

**Task:** audit the demo dataset and formalise the Inventory, Procurement and Supplier Intelligence MVP rules. **Estimated effort:** 6h. Approximately 1.5h of preceding functional analysis covered product purpose, scope, dataset strategy and initial rule selection; it is planning context, not exact engineering time.

## Work completed

- Added the reproducible CSV audit: [`scripts/audit_demo_data.py`](../../scripts/audit_demo_data.py).
- Audited all ten CSV datasets for business/primary-key uniqueness, nulls, relations, numeric, temporal and reconciliation controls.
- Recorded machine-generated evidence in [MVP_DATASET_AUDIT_RESULTS.md](MVP_DATASET_AUDIT_RESULTS.md).
- Formalised all 15 agreed MVP rules, including inputs, formulas, edge cases, configuration, action, demo evidence and limitations in [Business Rules](../04_BUSINESS_RULES.md).

## Evidence obtained

The corpus has 704 rows across ten CSVs: 1 company, 1 plant, 3 warehouses, 35 materials, 12 suppliers, 71 supplier-material relations, 35 inventory rows, 260 PO lines, 255 goods receipts and 31 requisitions. All declared business keys are unique; all audited foreign/business relationships have zero orphan references. All inventory quantities/costs are non-negative; purchase quantity and price are positive, transport is non-negative; all 255 RECEIVED lines have actual delivery dates and 5 OPEN lines do not.

Inventory availability and receipt accepted/rejected reconciliation pass using a 0.011 decimal tolerance. One inventory row has non-positive consumption: it is an expected business-rule edge case. The generated report is the source for counts and should be rerun after CSV changes.

## Findings

- **MEDIUM — persistence gap:** `plants`, `warehouses`, `supplier_materials`, `goods_receipts`, and `purchase_requisitions` exist in CSV but the current SQLAlchemy model and `load_demo_data.py` load only companies, materials, suppliers, inventory and purchase orders. This task deliberately does not extend the schema.
- **MEDIUM — recommendation definition gap:** eligibility can be checked from CSV, but a common normalisation for price, delivery, quality and reliability scores is not specified. A numeric recommendation must remain partial.
- **LOW — threshold calibration:** 60 target days, 90/180 movement days and ranking weights are demo/MVP configuration, not universal industrial defaults.
- **INFO — source versus calculated:** supplier quality and reliability fields are source scores. Acceptance rate can be calculated from receipts, but receipts are not persisted.
- **INFO — date reproducibility:** all rules requiring “today” are defined around an explicit `reference_date`.

## Business-rule status

| Rule | Status | Evidence | Remaining work |
| --- | --- | --- | --- |
| INV-001, INV-002, INV-004 to INV-007 | READY | Audited inventory columns and deterministic formulas | Implement runtime/UI when planned |
| INV-003 | PARTIAL | Safety-stock rule is ready; supplier lead time exists in CSV | Persist/query supplier-material eligibility/lead time |
| PROC-001, PROC-003, PROC-004, SUP-001, SUP-003 | READY | Audited PO/supplier fields and formal definitions | Implement runtime/UI when planned |
| PROC-002 | PARTIAL | Formula and historical source are defined | Define current-price/minimum-history policy and alert calibration |
| SUP-002 | PARTIAL | 255 receipts link and reconcile | Persist receipts; clarify source-score provenance |
| SUP-004 | PARTIAL | 71 supplier-material relations; PO pairs all valid | Define common score normalisation, MOQ demand basis and certification semantics |

## Decisions required to reach DONE

These are **functional decisions for closing this Step**. They do not authorise implementation of models, loaders, endpoints or services in this iteration.

1. **INV-003 — lead time:** decide whether `supplier_materials.lead_time_days` is used by the MVP stockout-risk condition; if yes, define selection of the eligible supplier/material relation when more than one exists. The safety-stock condition remains available independently.
2. **PROC-002 — price variation:** define the exact `current_price` record, the minimum qualifying historical observations, and the configurable threshold at which a variation produces an alert/review.
3. **SUP-002 — quality evidence:** choose the interim execution boundary for `goods_receipts`: direct CSV-backed calculation for the MVP demo, or a later persisted source. In both cases retain the distinction between `source_quality_score` and calculated acceptance rate.
4. **SUP-004 — recommendation:** define comparable normalisation for price, delivery, quality and reliability; final eligibility checks; MOQ demand basis; certification compatibility semantics; and ranking/tie behaviour. The current weights remain only an initial conceptual configuration.

## Subsequent work — explicitly not blocking this Step

- Adding SQLAlchemy models, migrations, loaders, APIs, services, endpoints or UI for plants, warehouses, supplier-material relations, receipts or requisitions.
- Implementing any Intelligence calculation in the runtime product after the above decisions are accepted.
- Calibrating thresholds and weights with public industrial, pilot or customer data. This is essential before production use, but is distinct from defining the functional MVP semantics required to close this documentation/audit Step.
- ML, forecasting, optimisation, LLM agents, C-MAPSS and Cognite work, all outside the current MVP scope.

## DoD checklist

| Requirement | Result |
| --- | --- |
| Dataset, relations, gaps and relevant fields audited | Complete, reproducible report |
| Inventory, Procurement and Supplier rules defined | Complete, 15 rule definitions |
| Inputs, formulas, edges, thresholds, interpretation, actions and demo examples | Complete in Business Rules |
| Source versus calculated distinction | Complete |
| Existing CSV data not loaded to PostgreSQL identified | Complete |
| Limits, evidence maturity and external lab boundary documented | Complete |
| Versioned documentation and audit script | Complete |
| Rule readiness sufficient for every agreed rule | Partial: the four explicit functional decisions above are pending |

## Final assessment: PARTIAL

The audit and formalisation work are complete, but the requested rule set cannot all be considered READY: recommendation normalisation is intentionally unspecified, quality receipts and lead-time relations need an agreed execution boundary, and price variation needs a selection/minimum-history policy. Before calling the whole Step DONE, Antonio/ChatGPT/Codex should approve the four functional decisions above. Persisting or productising those decisions is subsequent work and does not itself block this audit/documentation Step.

**Estimated remaining effort:** 1–2h for the four decisions and closure review. Persistence and product implementation should be estimated separately because they are subsequent scope.
