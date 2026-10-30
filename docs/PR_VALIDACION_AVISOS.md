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
- `python -m unittest discover -s tests -v`: 11 pruebas OK con Python 3.12 incluido en Codex.
- `git diff --check`: sin errores. No cambian eventos, permisos ni condiciones del workflow.

Es una entrega de preparación de COL-001; no completa sus entrevistas ni sus
criterios de producto. No cierra la Issue de prueba ni aprueba tareas. La prueba
valida el recorrido por etiqueta; no valida fallos críticos ni ejecución manual.
Sin cambios de permisos, tokens, protecciones ni configuración del teléfono.
