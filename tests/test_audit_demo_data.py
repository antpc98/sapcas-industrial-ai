from scripts.audit_demo_data import audit, load_data


def test_demo_audit_detects_clean_core_relationships() -> None:
    result = audit(load_data())

    assert result["counts"]["purchase_orders"] == 260
    assert not any(result["duplicate_keys"].values())
    assert not any(result["orphans"].values())
    assert result["inventory_reconciliation_failures"] == 0
    assert result["receipt_reconciliation_failures"] == 0
    assert result["purchase_invalid_supplier_material"] == 0
    assert result["receipt_orphan_purchase_line"] == 0
    assert not any(result["invalid_dates"].values())
