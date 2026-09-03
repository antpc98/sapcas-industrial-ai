# Reglas de negocio — documento vivo

Este documento delimita lo que debe formalizarse; no define umbrales, fórmulas finales ni comportamiento implementado.

## Inventory Intelligence

Objetivo: identificar faltantes, exceso y capital inmovilizado por material/ubicación.

- `available_stock`: validar relación entre físico, reservado y disponible.
- `days_of_inventory`: definir cobertura y casos de consumo cero.
- Riesgo de rotura: horizonte, stock de seguridad, criticidad y lead time.
- Sobrestock/slow moving: períodos, exclusiones y materiales sin consumo.
- Valor y capital excedente: coste, moneda y cálculo de exceso.

**TODO / TO BE DEFINED:** umbrales, alertas, redondeos, datos incompletos y validación contra escenarios demo.

## Procurement Intelligence

Objetivo: detectar precio desfavorable y medir coste de compra.

- Histórico y variación: ventana, comparador, moneda y cantidades.
- Coste efectivo: tratamiento de transporte y componentes adicionales.
- KPIs: agregación por empresa, planta, material o proveedor.
- Cumplimiento: fecha de referencia y pedidos abiertos/sin entrega real.

**TODO / TO BE DEFINED:** fórmulas, tolerancias, normalización monetaria y mínimo de datos.

## Supplier Intelligence

Objetivo: evaluar proveedor-material para apoyar compra o RFQ.

- Delivery performance desde fechas esperada/real.
- Calidad desde cantidades aceptadas/rechazadas.
- Elegibilidad/ranking: pesos, exclusiones, certificación, lead time, MOQ, precio y preferencia.

**TODO / TO BE DEFINED:** escalas, pesos, desempates, caducidad y explicabilidad.

Las reglas objetivas deben calcularse con datos, SQL y Python. Una capa de lenguaje futura explicará resultados, no los sustituirá.
