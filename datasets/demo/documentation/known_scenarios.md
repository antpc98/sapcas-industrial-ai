# Known Scenarios v0.1

Estos escenarios son deliberados y servirán como tests del motor.

## SCN-001 — Excess stock
**Material:** AL-6082-T6-BAR  
**Expected:** EXCESS_STOCK  
**Reason:** ~173 días de cobertura antes de reservas.

## SCN-002 — Shortage risk
**Material:** AL-7075-T6-PLATE  
**Expected:** SHORTAGE_RISK  
**Reason:** ~9 días de cobertura y proveedores con lead time superior/parecido.

## SCN-003 — Dead stock
**Material:** BEARING-6004  
**Expected:** DEAD_STOCK  
**Reason:** consumo medio 0 y último movimiento hace ~211 días.

## SCN-004 — Reserved stock risk
**Material:** FAST-M6-AERO  
**Expected:** AVAILABLE_STOCK_RISK  
**Reason:** 500 unidades físicas, 430 reservadas; sólo 70 disponibles.

## SCN-005 — Single source risk
**Material:** FAST-M8-AERO  
**Expected:** SINGLE_SOURCE_RISK  
**Reason:** un único proveedor disponible en supplier_materials.

## SCN-006 — Rising price trend
**Material:** INOX-AISI316L  
**Expected:** PRICE_INCREASE_TREND  
**Reason:** histórico de PO generado con incremento progresivo desde 2025.

## SCN-007 — Supplier delivery degradation
**Supplier:** SUP-006  
**Expected:** DELIVERY_RELIABILITY_DEGRADATION  
**Reason:** se introducen más retrasos deliberadamente en los últimos 3 meses.

## SCN-008 — Supplier quality trade-off
**Supplier:** SUP-006  
**Expected:** QUALITY_RISK  
**Reason:** mayor ratio de cantidad rechazada en recepciones que otros proveedores.

## SCN-009 — MOQ / excess risk
**Supplier:** SUP-012  
**Expected:** MOQ_EXCESS_RISK  
**Reason:** MOQ deliberadamente superior y lead time largo, aunque precios competitivos.

## SCN-010 — Procurement urgency
**Material:** AL-7075-T6-PLATE  
**Requisition:** PR-0099  
**Expected:** RFQ_OR_ORDER_PRIORITY  
**Reason:** necesidad en 13 días sobre material con cobertura limitada.
