Auditoría final de COL-006 (Issue #19), posterior a las preparaciones P0 integradas por el propietario.

- p0_status.py solo lee registros y aceptación GitHub. Detecta duplicados, no infiere approved de merges y nunca autoriza P1.
- Checkpoint ESTADO_AGENTE actualizado con ramas, pruebas, entregas, bloqueos e instrucciones de reanudación.
- Refuerzo menor del validador de dataset: basis debe ser texto no vacío; se añade prueba negativa.
- Documentación de modo manual de avisos corregida al formato real; sin cambios de permisos o configuración sensible.
- 64 unittest locales OK; comandos reales --ready devuelven 2, con cero entrevistas/pares/ejecuciones. Sin datos inventados, nuevas dependencias ni motor.

Las Issues y los registros reales permanecen abiertos/incompletos. Se requiere revisión del instrumento y datos reales; no cierre automático, approved o merge por el agente. Los enlaces de CI y solicitud consolidada se registran en la Issue tras publicar.
