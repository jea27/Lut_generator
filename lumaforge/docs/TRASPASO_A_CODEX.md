# Traspaso completo de contexto a Codex · 30 octubre 2026

> Este documento conserva decisiones expresadas por el usuario en la conversación con ChatGPT. No implica que esas funciones estén programadas. Para el estado real, revisa el repositorio y GitHub.

## Necesidad original
El usuario quiere dar una foto de referencia y conseguir automáticamente un preset para aplicar el mismo *look* a sus imágenes. Requiere que funcione en Photoshop, pero además en edición de vídeo y otras plataformas. Desea evitar quedar encerrado en el ecosistema Adobe.

## Decisión principal: IA mínima
No generar cada imagen con modelos generativos ni pagar por inferencia por imagen sin necesidad. El pipeline previsto:
1. La referencia se analiza con histograma, paleta, contraste, curvas, canales, HSL y otras estadísticas perceptuales.
2. Se genera una **receta de look reutilizable** y un LUT 3D (.cube) donde sea apropiado.
3. Cada imagen destino se normaliza/adapta con algoritmos clásicos. La LUT por sí sola no representa máscaras, ajustes espaciales ni exposición contextual.
4. Opcionalmente, pequeños modelos locales detectan cielo, piel o sujeto y ayudan a preservar regiones; **no** lanzar API externa salvo consentimiento/coste aprobado.
5. Cachear análisis de referencias; reutilizarlo en lote.
6. En vídeo, muestrear fotogramas, agrupar por planos, suavizar cambios en el tiempo y controlar explícitamente gamma/espacios de color.

## Producto y UX
- Una referencia (foto o frame) + imágenes/vídeo de usuario.
- Previsualización antes/después, intensidad, edición de curvas/ajustes, biblioteca de looks y exportación.
- Separar *estilo global*, *receta de adaptación* y *resultado renderizado*. No prometer recuperación exacta del preset original.
- Modos previstos: rápido determinista; inteligente local; avanzado con proveedor externo opcional.
- Primer público hipotético: fotógrafos, videógrafos y creadores individuales; validar antes de construir una suscripción comercial.

## Arquitectura acordada
- UI: Vue 3 + TypeScript + Quasar, accesible en navegador inicialmente.
- Motor: Python/FastAPI, NumPy/OpenCV, OpenColorIO para gestión de color, FFmpeg para vídeo.
- Inferencia opcional: ONNX Runtime o PyTorch local, con requisitos de hardware modestos y modo CPU.
- Distribución: Windows primero, empaquetado futuro Tauri cuando el motor lo permita.
- LUT .cube primero para Photoshop, Premiere y DaVinci; XMP y conectores específicos como ampliaciones posteriores, con pruebas de compatibilidad.
- SQLite + JSON para biblioteca local; nunca publicar medios privados por defecto.
- GitHub como fuente de estado de ejecución. Web estática tipo Project OS para ver fases, tareas, mercado, riesgos y comentarios.

## Investigación previa / limitaciones
Se revisaron competidores con ofertas distintas: Colourlab Ai, Luttie, fylm.ai, Neurapix, Imagen y Aftershoot. Que existan competidores valida la categoría, **no** demuestra demanda para nuestra propuesta. `docs/ESTUDIO_DE_MERCADO.md` contiene precios y enlaces de referencia fechados; volver a comprobar antes de citar precios actuales.

Riesgos primarios: ambigüedad referencia vs iluminación propia de escena; gestión de color RAW/Log/Rec.709, gamma y gamut; parpadeos en vídeo; derechos/licencias; tamaño y rendimiento; coste y precisión del modelo local; privacidad de imágenes; complejidad de exportar XMP.

## Decisiones operativas confirmadas
El usuario quiere **traspasar el proyecto a Codex local en Windows**, que trabaje por tareas, documente todo, haga push **al completar entregas revisables**, actualice la hoja de ruta automáticamente y avise al móvil cuando necesite intervención humana o autorización. El usuario revisará y corregirá entregas. No confundir autonomía de trabajo con autorización para publicar a producción, fusionar cambios a main o incurrir en gastos.

## Estado heredado REAL
- Hay **42 tareas** y seis fases P0–P5 en `site/data/roadmap.json`.
- Existe dashboard estático (site/) con datos iniciales; integración de lectura con GitHub Actions/Issues/PR si se publica.
- Hay 8 pruebas originales del sincronizador (verificar mediante tests); **no** existe aún motor funcional de foto/vídeo ni IA adaptativa.
- No hay URL pública ni repositorio externo configurado en los archivos iniciales.
- Documentos previos: `docs/ARQUITECTURA.md`, `docs/ESTUDIO_DE_MERCADO.md`, `docs/OPERATIVA_CON_IA.md`.

## Fases e hitos
- P0: validación de usuarios, benchmark y casos de referencia; permiso humano para decisiones de producto.
- P1: motor determinista, gestión de color, tests reproducibles y LUT .cube.
- P2: interfaz de edición funcional y biblioteca.
- P3: adaptación inteligente local opcional; medir mejora frente a baseline.
- P4: soporte vídeo, coherencia temporal y exportación.
- P5: distribución Windows, QA, beta e integraciones.
Las semanas indicadas en el dashboard son estimativas, nunca plazos garantizados.

## Preferencias de trabajo del usuario
Es desarrollador web en Windows y trabaja con IntelliJ IDEA y Codex. Prefiere instrucciones y comandos concretos, fragmentos completos para copiar/pegar, informes de cambios y no alterar Git sin una política de permiso clara. Debe poder corregir decisiones sin que la IA se autoapruebe.

## Próxima sesión esperada de Codex
No comenzar creando un editor complejo. Primero auditar el starter, confirmar Git/GitHub y reglas de seguridad, crear/importar las Issues tras autorización, activar sincronización y push móvil y validar todo con una Issue de prueba. Después proponer P0 y la primera tarea técnica pequeña.
