Preparación parcial de COL-003, Issue #17: protocolo reproducible, revisión de
fuentes primarias y registro vacío con validador de comparabilidad/integridad
de referencias. No implementa motor de color ni ejecuta cinco competidores.

Fija los mismos 20 pares y distingue 100 casos automáticos de ajustes manuales.
No computa resultados desde publicidad ni convierte accesos bloqueados en
fallos de calidad. Documenta requisitos contradictorios de Colourlab y los
límites de documentación comercial frente a ejecución real.

Pruebas: duplicados, hashes de entrada inconsistentes, tiempo inválido,
evidencia/versiones/fechas ausentes, modos separados y registro vacío. Los
fixtures de 100 registros nunca se escriben al conjunto real ni son benchmark.
36 unittest locales OK (nueve nuevas); resultados de CI se registran en la Issue.

Intervención futura: aportar dataset autorizado y acceso a los productos, o
acordar una sustitución de un candidato inaccesible. No se instalan herramientas,
aceptan contratos ni suben imágenes a terceros sin permiso. La PR no cierra la
Issue ni aprueba P0. Fuentes y límites en docs/P0_COL-003_BENCHMARK.md.
