# Roadmap por fases

No hay fechas comprometidas. El orden y dependencias son:

1. **Base actual:** dataset, modelos, migración, carga y API de consulta.
2. **Definición de reglas:** métricas, fórmulas, umbrales, fuentes y aceptación. **Completada para Supply Chain v1.**
3. **Inventory Intelligence:** implementar cobertura, riesgo, exceso, movimiento y valor definidos.
4. **Procurement Intelligence:** precio, coste y cumplimiento.
5. **Supplier Intelligence:** desempeño, calidad, elegibilidad y ranking.
6. **RFQ/recomendaciones:** priorizar necesidades y candidatos explicables.
7. **Demo comercial:** escenarios controlados y resultados verificables.

Las fases 3–6 dependen de las reglas. Supplier/RFQ pueden iniciar ejecución demo desde CSV, pero la implementación productiva depende de decidir y modelar/cargar `supplier_materials`, `goods_receipts` y `purchase_requisitions`. La calibración con cliente y los laboratorios externos son roadmap separado.
