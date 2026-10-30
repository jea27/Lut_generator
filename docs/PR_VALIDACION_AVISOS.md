Se ha validado el aviso humano real de LumaForge: REVIEWER_GITHUB ya contiene
jea27; al etiquetar la Issue #3 con needs-human, Actions publicó la mención y
el usuario confirmó «Sí, recibida en el móvil».

Esta PR documenta la evidencia y ajusta AGENTS, el protocolo y el texto del bot
para detener solo el trabajo que depende de la decisión y continuar tareas
independientes autorizadas. La recepción del aviso nunca implica aprobación.

Evidencia:
- Issue de prueba: https://github.com/jea27/Lut_generator/issues/3
- Run real con success: https://github.com/jea27/Lut_generator/actions/runs/41079364488
- Mención: https://github.com/jea27/Lut_generator/issues/3#issuecomment-6526303053
- Confirmación registrada: https://github.com/jea27/Lut_generator/issues/3#issuecomment-6526329955
- El primer aviso de PR falló con 403 al comentar sobre la propia PR. Sin ampliar permisos, ahora crea una Issue de revisión y publica allí la mención. Se añade synchronize y deduplicación por PR.
- Prueba real de la corrección: https://github.com/jea27/Lut_generator/actions/runs/41080088759 (success).
- Issue de revisión creada por el bot: https://github.com/jea27/Lut_generator/issues/5; mención: https://github.com/jea27/Lut_generator/issues/5#issuecomment-6526363671.
- CI: https://github.com/jea27/Lut_generator/actions/runs/41080088573 (validate success, publish omitido desde PR).
- Pruebas locales adicionales ejecutan el script exacto del workflow con API simulada: creación en Issue, etiquetas, mención, deduplicación y login inválido.
- Suite final: `python -m unittest discover -s tests -v`, 15 pruebas OK.
- `git diff --check`: sin errores. Sin cambios de permisos del workflow o del repositorio.

Es una entrega de preparación de COL-001; no completa sus entrevistas ni sus
criterios de producto. No cierra la Issue de prueba ni aprueba tareas. La prueba
valida el recorrido por etiqueta; no valida fallos críticos ni ejecución manual.
Sin cambios de permisos, tokens, protecciones ni configuración del teléfono.
