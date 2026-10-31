window.INITIAL_PRODUCT = {
  "schema_version": 1,
  "product": "Color Studio",
  "sync": {
    "status": "complete",
    "observed_at": "2026-10-31T10:06:42.993325Z",
    "main_sha": "448a1015c1f0b424a9ed85a50a52a542d7e03acd"
  },
  "source_version": "0.3.0-beta.2",
  "candidate": {
    "version": "0.3.0-beta.2",
    "sha256": "3e3851ee4f3c67608d3802ad167572375b130eeafa57165d26379cd26797714f",
    "source": "a452a5f9a1d5eab80b60219cb1ad9fdad60c1b46",
    "bytes": 266211731,
    "dirty": false,
    "signature": "NotSigned",
    "clean_windows": false,
    "evidence_url": "https://github.com/jea27/Lut_generator/blob/main/docs/evidence/LOOK_03_ARTIFACT_B2.json"
  },
  "latest_release": null,
  "versions": [
    {
      "version": "0.3.0-beta.2",
      "sha256": "3e3851ee4f3c67608d3802ad167572375b130eeafa57165d26379cd26797714f",
      "source": "a452a5f9a1d5eab80b60219cb1ad9fdad60c1b46",
      "bytes": 266211731,
      "dirty": false,
      "signature": "NotSigned",
      "clean_windows": false,
      "evidence_url": "https://github.com/jea27/Lut_generator/blob/main/docs/evidence/LOOK_03_ARTIFACT_B2.json"
    },
    {
      "version": "0.3.0-beta.1",
      "sha256": "ae47f44e6f9382810e20a7a98b0b46bf6d53411e7f1c8b0fb2e9c7acf595ac21",
      "source": "396a508a7cd918598b378becf175e0ddaf3aa2f9",
      "bytes": 266203035,
      "dirty": false,
      "signature": "NotSigned",
      "clean_windows": false,
      "evidence_url": "https://github.com/jea27/Lut_generator/blob/main/docs/evidence/LOOK_03_ARTIFACT.json"
    },
    {
      "version": "0.2.0-beta.1",
      "sha256": "c1798ece22b9a8f38b6c7042a59630c16800b7a7ca295ee4119a8c157d092a4a",
      "source": "f8788dbbcdab619aafdfd7f1e6ddaee52573f311",
      "bytes": 266193722,
      "dirty": true,
      "signature": "NotSigned",
      "clean_windows": false,
      "evidence_url": "https://github.com/jea27/Lut_generator/blob/main/docs/evidence/BETA_02_ARTIFACT.json"
    }
  ],
  "features": [
    {
      "id": "color-match",
      "title": "Color Match",
      "group": "MVP",
      "task": "COL-011",
      "acceptance": "Estadísticas Lab acotadas, intensidad y render mediante la misma LUT33³.",
      "status": "review",
      "implemented": true,
      "technically_verified": true,
      "human_approved": false,
      "blocked": false,
      "issue_url": "https://github.com/jea27/Lut_generator/issues/43",
      "pr_url": "https://github.com/jea27/Lut_generator/pull/70",
      "evidence": [
        {
          "label": "Prueba",
          "url": "https://github.com/jea27/Lut_generator/blob/main/tests_mvp/test_engine.py"
        }
      ],
      "review": {
        "state": "pending",
        "context": {
          "commit": "015fc895f56e684daff7527290123e2233a7d30c",
          "version": "0.3.0-beta.2",
          "revision": "2b3706b7d54d421506ca1a991605f21f17552a6b9cfe6915c3aeccce2d8aea06"
        },
        "history": [],
        "latest": null
      },
      "review_steps": [
        "Abrir demo local o dos fotos propias autorizadas y ejecutar Analizar y transferir.",
        "Mover intensidad de color a0 y100: comparar la misma foto al100% y comprobar tonos/extremos."
      ],
      "checklist": [
        {
          "id": "behavior",
          "label": "El comportamiento descrito funciona en mi prueba."
        },
        {
          "id": "quality",
          "label": "He comparado el resultado y no encuentro un fallo bloqueante en este alcance."
        },
        {
          "id": "evidence",
          "label": "He comprobado versión, evidencias y limitaciones de la entrega."
        }
      ],
      "verification_scope": "Tests de main y evidencia versionada; no aceptación estética ni Windows limpio"
    },
    {
      "id": "manual-look",
      "title": "Look Match manual",
      "group": "MVP",
      "task": "COL-026",
      "acceptance": "Glow, difusión y fade manuales; no inferencia automática fiel de referencia.",
      "status": "review",
      "implemented": true,
      "technically_verified": true,
      "human_approved": false,
      "blocked": false,
      "issue_url": "https://github.com/jea27/Lut_generator/issues/68",
      "pr_url": "https://github.com/jea27/Lut_generator/pull/70",
      "evidence": [
        {
          "label": "Prueba",
          "url": "https://github.com/jea27/Lut_generator/blob/main/tests_mvp/test_look.py"
        },
        {
          "label": "Evidencia",
          "url": "https://github.com/jea27/Lut_generator/blob/main/docs/evidence/LOOK_03_FROZEN_B2.json"
        }
      ],
      "review": {
        "state": "pending",
        "context": {
          "commit": "015fc895f56e684daff7527290123e2233a7d30c",
          "version": "0.3.0-beta.2",
          "revision": "9806827f40df0204cb6ba22dd050e1b5182e0e9ba55882ed2115d22a1d67c4e4"
        },
        "history": [],
        "latest": null
      },
      "review_steps": [
        "Aplicar el acabado con y sin su interruptor, variando intensidad.",
        "Guardar receta, volver a cargarla y exportar PNG; comprobar que LUT solo incluye color."
      ],
      "checklist": [
        {
          "id": "behavior",
          "label": "El comportamiento descrito funciona en mi prueba."
        },
        {
          "id": "quality",
          "label": "He comparado el resultado y no encuentro un fallo bloqueante en este alcance."
        },
        {
          "id": "evidence",
          "label": "He comprobado versión, evidencias y limitaciones de la entrega."
        }
      ],
      "verification_scope": "Tests de main y evidencia versionada; no aceptación estética ni Windows limpio"
    },
    {
      "id": "glow",
      "title": "Glow en altas luces",
      "group": "Componente",
      "task": "COL-026",
      "acceptance": "Componente de Look Match: luz lineal, radio relativo, bypass e intensidad.",
      "status": "review",
      "implemented": true,
      "technically_verified": true,
      "human_approved": false,
      "blocked": false,
      "issue_url": "https://github.com/jea27/Lut_generator/issues/68",
      "pr_url": "https://github.com/jea27/Lut_generator/pull/70",
      "evidence": [
        {
          "label": "Prueba",
          "url": "https://github.com/jea27/Lut_generator/blob/main/tests_mvp/test_look.py"
        }
      ],
      "review": {
        "state": "pending",
        "context": {
          "commit": "015fc895f56e684daff7527290123e2233a7d30c",
          "version": "0.3.0-beta.2",
          "revision": "8950eceb49fcd4b0145d4c0597c80abb5a9d308285ee3727114ec77d2908d38c"
        },
        "history": [],
        "latest": null
      },
      "review_steps": [
        "Usar foto con altas luces. Activar solo Glow; Difusión y Fade a0.",
        "Comparar radio e intensidad, revisar halos/bordes y desactivar para recuperar la base."
      ],
      "checklist": [
        {
          "id": "behavior",
          "label": "El comportamiento descrito funciona en mi prueba."
        },
        {
          "id": "quality",
          "label": "He comparado el resultado y no encuentro un fallo bloqueante en este alcance."
        },
        {
          "id": "evidence",
          "label": "He comprobado versión, evidencias y limitaciones de la entrega."
        }
      ],
      "verification_scope": "Tests de main y evidencia versionada; no aceptación estética ni Windows limpio"
    },
    {
      "id": "diffusion",
      "title": "Difusión",
      "group": "Componente",
      "task": "COL-026",
      "acceptance": "Suavizado con alfa y halos entre tiles; forma parte de la receta, no LUT.",
      "status": "review",
      "implemented": true,
      "technically_verified": true,
      "human_approved": false,
      "blocked": false,
      "issue_url": "https://github.com/jea27/Lut_generator/issues/68",
      "pr_url": "https://github.com/jea27/Lut_generator/pull/70",
      "evidence": [
        {
          "label": "Prueba",
          "url": "https://github.com/jea27/Lut_generator/blob/main/tests_mvp/test_look.py"
        }
      ],
      "review": {
        "state": "pending",
        "context": {
          "commit": "015fc895f56e684daff7527290123e2233a7d30c",
          "version": "0.3.0-beta.2",
          "revision": "a9e9a11f8a999c4443a98e4695685e63f497c5b3ea9ffad1005fecc6f88cf682"
        },
        "history": [],
        "latest": null
      },
      "review_steps": [
        "Activar solo Difusión sobre foto con detalle fino; Glow y Fade a0.",
        "Examinar bordes al100%, variar intensidad/radio y comprobar bypass."
      ],
      "checklist": [
        {
          "id": "behavior",
          "label": "El comportamiento descrito funciona en mi prueba."
        },
        {
          "id": "quality",
          "label": "He comparado el resultado y no encuentro un fallo bloqueante en este alcance."
        },
        {
          "id": "evidence",
          "label": "He comprobado versión, evidencias y limitaciones de la entrega."
        }
      ],
      "verification_scope": "Tests de main y evidencia versionada; no aceptación estética ni Windows limpio"
    },
    {
      "id": "fade",
      "title": "Fade",
      "group": "Componente",
      "task": "COL-026",
      "acceptance": "Elevación de negros y compresión acotada, conservadas en receta completa.",
      "status": "review",
      "implemented": true,
      "technically_verified": true,
      "human_approved": false,
      "blocked": false,
      "issue_url": "https://github.com/jea27/Lut_generator/issues/68",
      "pr_url": "https://github.com/jea27/Lut_generator/pull/70",
      "evidence": [
        {
          "label": "Prueba",
          "url": "https://github.com/jea27/Lut_generator/blob/main/tests_mvp/test_look.py"
        }
      ],
      "review": {
        "state": "pending",
        "context": {
          "commit": "015fc895f56e684daff7527290123e2233a7d30c",
          "version": "0.3.0-beta.2",
          "revision": "09054ba6a6d7677255182ed2cd65c6d2bf5244e73221ff00d8554a3e28165d03"
        },
        "history": [],
        "latest": null
      },
      "review_steps": [
        "Activar solo Fade con sombras y luces visibles.",
        "Comprobar elevación gradual de negros, ausencia de saltos y bypass."
      ],
      "checklist": [
        {
          "id": "behavior",
          "label": "El comportamiento descrito funciona en mi prueba."
        },
        {
          "id": "quality",
          "label": "He comparado el resultado y no encuentro un fallo bloqueante en este alcance."
        },
        {
          "id": "evidence",
          "label": "He comprobado versión, evidencias y limitaciones de la entrega."
        }
      ],
      "verification_scope": "Tests de main y evidencia versionada; no aceptación estética ni Windows limpio"
    },
    {
      "id": "presets",
      "title": "Biblioteca de presets",
      "group": "MVP",
      "task": "COL-018",
      "acceptance": "Guardar, aplicar, editar, agrupar y conservar presets locales.",
      "status": "progress",
      "implemented": true,
      "technically_verified": true,
      "human_approved": false,
      "blocked": false,
      "issue_url": "https://github.com/jea27/Lut_generator/issues/50",
      "pr_url": "https://github.com/jea27/Lut_generator/pull/65",
      "evidence": [
        {
          "label": "Prueba",
          "url": "https://github.com/jea27/Lut_generator/blob/main/tests_mvp/test_beta.py"
        }
      ],
      "review": {
        "state": "pending",
        "context": {
          "commit": "015fc895f56e684daff7527290123e2233a7d30c",
          "version": "0.3.0-beta.2",
          "revision": "ae5da8f7c9de4976022e88669f0b4641e6ae5540623858fb9229bdd0614ac8a9"
        },
        "history": [],
        "latest": null
      },
      "review_steps": [
        "Guardar un preset de prueba, renombrar y mover de grupo.",
        "Cerrar/abrir la app y aplicarlo de nuevo; eliminar únicamente el preset de ensayo."
      ],
      "checklist": [
        {
          "id": "behavior",
          "label": "El comportamiento descrito funciona en mi prueba."
        },
        {
          "id": "quality",
          "label": "He comparado el resultado y no encuentro un fallo bloqueante en este alcance."
        },
        {
          "id": "evidence",
          "label": "He comprobado versión, evidencias y limitaciones de la entrega."
        }
      ],
      "verification_scope": "Tests de main y evidencia versionada; no aceptación estética ni Windows limpio"
    },
    {
      "id": "batches",
      "title": "Procesamiento por lotes",
      "group": "MVP",
      "task": "COL-037",
      "acceptance": "Lotes cancelables con outputs separados y recuperación interrupted.",
      "status": "review",
      "implemented": true,
      "technically_verified": true,
      "human_approved": false,
      "blocked": false,
      "issue_url": "https://github.com/jea27/Lut_generator/issues/58",
      "pr_url": "https://github.com/jea27/Lut_generator/pull/65",
      "evidence": [
        {
          "label": "Prueba",
          "url": "https://github.com/jea27/Lut_generator/blob/main/tests_mvp/test_beta.py"
        },
        {
          "label": "Evidencia",
          "url": "https://github.com/jea27/Lut_generator/blob/main/docs/evidence/LOOK_03_FROZEN_B2.json"
        }
      ],
      "review": {
        "state": "pending",
        "context": {
          "commit": "015fc895f56e684daff7527290123e2233a7d30c",
          "version": "0.3.0-beta.2",
          "revision": "a617db0f24655b6f546d7e9bf53bf989d3bdaeb8aa3b63dfc1b412f21e0e3b15"
        },
        "history": [],
        "latest": null
      },
      "review_steps": [
        "Con dos copias autorizadas, aplicar una receta al lote y exportar.",
        "Comparar salida individual, cancelar otro ensayo y comprobar originales intactos."
      ],
      "checklist": [
        {
          "id": "behavior",
          "label": "El comportamiento descrito funciona en mi prueba."
        },
        {
          "id": "quality",
          "label": "He comparado el resultado y no encuentro un fallo bloqueante en este alcance."
        },
        {
          "id": "evidence",
          "label": "He comprobado versión, evidencias y limitaciones de la entrega."
        }
      ],
      "verification_scope": "Tests de main y evidencia versionada; no aceptación estética ni Windows limpio"
    },
    {
      "id": "lut-export",
      "title": "Exportación LUT de color",
      "group": "MVP",
      "task": "COL-012",
      "acceptance": "LUT33³ sRGB global; no transporta glow, difusión, fade o adaptación local.",
      "status": "review",
      "implemented": true,
      "technically_verified": true,
      "human_approved": false,
      "blocked": false,
      "issue_url": "https://github.com/jea27/Lut_generator/issues/44",
      "pr_url": "https://github.com/jea27/Lut_generator/pull/70",
      "evidence": [
        {
          "label": "Prueba",
          "url": "https://github.com/jea27/Lut_generator/blob/main/tests_mvp/test_engine.py"
        },
        {
          "label": "Evidencia",
          "url": "https://github.com/jea27/Lut_generator/blob/main/docs/evidence/LOOK_03_FROZEN_B2.json"
        }
      ],
      "review": {
        "state": "pending",
        "context": {
          "commit": "015fc895f56e684daff7527290123e2233a7d30c",
          "version": "0.3.0-beta.2",
          "revision": "6eb9baa80448a574f05fc4aa51655c59d2ac6da230ba3ae51b4fbf40d9cb7894"
        },
        "history": [],
        "latest": null
      },
      "review_steps": [
        "Exportar .cube y comprobar el aviso de solo color.",
        "Comparar con render de color, sin esperar glow/difusión/fade dentro de LUT."
      ],
      "checklist": [
        {
          "id": "behavior",
          "label": "El comportamiento descrito funciona en mi prueba."
        },
        {
          "id": "quality",
          "label": "He comparado el resultado y no encuentro un fallo bloqueante en este alcance."
        },
        {
          "id": "evidence",
          "label": "He comprobado versión, evidencias y limitaciones de la entrega."
        }
      ],
      "verification_scope": "Tests de main y evidencia versionada; no aceptación estética ni Windows limpio"
    },
    {
      "id": "image-export",
      "title": "Exportación PNG/JPG",
      "group": "MVP",
      "task": "COL-019",
      "acceptance": "Resolución original, ICC sRGB, originales intactos y acabado completo.",
      "status": "review",
      "implemented": true,
      "technically_verified": true,
      "human_approved": false,
      "blocked": false,
      "issue_url": "https://github.com/jea27/Lut_generator/issues/51",
      "pr_url": "https://github.com/jea27/Lut_generator/pull/70",
      "evidence": [
        {
          "label": "Prueba",
          "url": "https://github.com/jea27/Lut_generator/blob/main/tests_mvp/test_api.py"
        },
        {
          "label": "Evidencia",
          "url": "https://github.com/jea27/Lut_generator/blob/main/docs/evidence/LOOK_03_FROZEN_B2.json"
        }
      ],
      "review": {
        "state": "pending",
        "context": {
          "commit": "015fc895f56e684daff7527290123e2233a7d30c",
          "version": "0.3.0-beta.2",
          "revision": "1ebe1f3fbe91ae0d20589afee93342719dd164e5a9191add14546110d94b1fa5"
        },
        "history": [],
        "latest": null
      },
      "review_steps": [
        "Exportar PNG/JPG desde foto autorizada y revisar dimensiones y perfil sRGB.",
        "Comparar al100% con la vista, preservación de originales y acabado."
      ],
      "checklist": [
        {
          "id": "behavior",
          "label": "El comportamiento descrito funciona en mi prueba."
        },
        {
          "id": "quality",
          "label": "He comparado el resultado y no encuentro un fallo bloqueante en este alcance."
        },
        {
          "id": "evidence",
          "label": "He comprobado versión, evidencias y limitaciones de la entrega."
        }
      ],
      "verification_scope": "Tests de main y evidencia versionada; no aceptación estética ni Windows limpio"
    },
    {
      "id": "recipe",
      "title": "Receta JSON versionada",
      "group": "MVP",
      "task": "COL-018",
      "acceptance": "Receta v2 con acabado; compatible con v1 sin efectos.",
      "status": "progress",
      "implemented": true,
      "technically_verified": true,
      "human_approved": false,
      "blocked": false,
      "issue_url": "https://github.com/jea27/Lut_generator/issues/50",
      "pr_url": "https://github.com/jea27/Lut_generator/pull/70",
      "evidence": [
        {
          "label": "Prueba",
          "url": "https://github.com/jea27/Lut_generator/blob/main/tests_mvp/test_look.py"
        },
        {
          "label": "Evidencia",
          "url": "https://github.com/jea27/Lut_generator/blob/main/docs/evidence/LOOK_03_FROZEN_B2.json"
        }
      ],
      "review": {
        "state": "pending",
        "context": {
          "commit": "015fc895f56e684daff7527290123e2233a7d30c",
          "version": "0.3.0-beta.2",
          "revision": "75cdb0a1f03e16d03882c393f086dc6f146d18506ebf8f9eb2a22792f0d984e6"
        },
        "history": [],
        "latest": null
      },
      "review_steps": [
        "Exportar receta con efectos, cargarla y comparar los controles/resultados.",
        "Aplicar presetv1, activar acabado y exportar JSONv2 conservando el color."
      ],
      "checklist": [
        {
          "id": "behavior",
          "label": "El comportamiento descrito funciona en mi prueba."
        },
        {
          "id": "quality",
          "label": "He comparado el resultado y no encuentro un fallo bloqueante en este alcance."
        },
        {
          "id": "evidence",
          "label": "He comprobado versión, evidencias y limitaciones de la entrega."
        }
      ],
      "verification_scope": "Tests de main y evidencia versionada; no aceptación estética ni Windows limpio"
    },
    {
      "id": "windows",
      "title": "Aplicación Windows",
      "group": "MVP",
      "task": "COL-036",
      "acceptance": "Tauri/NSIS y sidecar. Verificación local; Windows limpio sigue pendiente.",
      "status": "review",
      "implemented": true,
      "technically_verified": true,
      "human_approved": false,
      "blocked": false,
      "issue_url": "https://github.com/jea27/Lut_generator/issues/57",
      "pr_url": "https://github.com/jea27/Lut_generator/pull/65",
      "evidence": [
        {
          "label": "Prueba",
          "url": "https://github.com/jea27/Lut_generator/blob/main/tests_mvp/test_beta.py"
        },
        {
          "label": "Evidencia",
          "url": "https://github.com/jea27/Lut_generator/blob/main/docs/evidence/LOOK_03_INSTALL_B2.json"
        }
      ],
      "review": {
        "state": "pending",
        "context": {
          "commit": "015fc895f56e684daff7527290123e2233a7d30c",
          "version": "0.3.0-beta.2",
          "revision": "06d10e0663b864bd772c4412e8ccd368d6813204265fe0bd3457d23dab09b2e5"
        },
        "history": [],
        "latest": null
      },
      "review_steps": [
        "Ejecutar protocolo de QA en el equipo de prueba autorizado.",
        "Comprobar instalación, arranque, cierre, presets y actualización sin perder datos; declarar entorno probado."
      ],
      "checklist": [
        {
          "id": "behavior",
          "label": "El comportamiento descrito funciona en mi prueba."
        },
        {
          "id": "quality",
          "label": "He comparado el resultado y no encuentro un fallo bloqueante en este alcance."
        },
        {
          "id": "evidence",
          "label": "He comprobado versión, evidencias y limitaciones de la entrega."
        }
      ],
      "verification_scope": "Tests de main y evidencia versionada; no aceptación estética ni Windows limpio"
    },
    {
      "id": "adobe",
      "title": "Compatibilidad Photoshop / Premiere",
      "group": "Integración",
      "task": "COL-038",
      "acceptance": "Requiere importación y comparación real en editores activados y dominio sRGB.",
      "status": "blocked",
      "implemented": false,
      "technically_verified": false,
      "human_approved": false,
      "blocked": true,
      "issue_url": "https://github.com/jea27/Lut_generator/issues/59",
      "pr_url": null,
      "evidence": [],
      "review": {
        "state": "pending",
        "context": null,
        "history": [],
        "latest": null
      },
      "review_steps": [
        "Esta capacidad todavía no tiene una entrega revisable."
      ],
      "checklist": [
        {
          "id": "behavior",
          "label": "El comportamiento descrito funciona en mi prueba."
        },
        {
          "id": "quality",
          "label": "He comparado el resultado y no encuentro un fallo bloqueante en este alcance."
        },
        {
          "id": "evidence",
          "label": "He comprobado versión, evidencias y limitaciones de la entrega."
        }
      ],
      "verification_scope": "Tests de main y evidencia versionada; no aceptación estética ni Windows limpio"
    },
    {
      "id": "resolve",
      "title": "Compatibilidad DaVinci Resolve",
      "group": "Integración",
      "task": "COL-038",
      "acceptance": "Requiere prueba real de LUT, interpolación, niveles y espacio de color.",
      "status": "blocked",
      "implemented": false,
      "technically_verified": false,
      "human_approved": false,
      "blocked": true,
      "issue_url": "https://github.com/jea27/Lut_generator/issues/59",
      "pr_url": null,
      "evidence": [],
      "review": {
        "state": "pending",
        "context": null,
        "history": [],
        "latest": null
      },
      "review_steps": [
        "Esta capacidad todavía no tiene una entrega revisable."
      ],
      "checklist": [
        {
          "id": "behavior",
          "label": "El comportamiento descrito funciona en mi prueba."
        },
        {
          "id": "quality",
          "label": "He comparado el resultado y no encuentro un fallo bloqueante en este alcance."
        },
        {
          "id": "evidence",
          "label": "He comprobado versión, evidencias y limitaciones de la entrega."
        }
      ],
      "verification_scope": "Tests de main y evidencia versionada; no aceptación estética ni Windows limpio"
    },
    {
      "id": "automatic-look",
      "title": "Detección automática del acabado",
      "group": "Futuro",
      "task": "COL-026",
      "acceptance": "Inferir parámetros desde referencia, incertidumbre y revisión visual; posterior a beta.",
      "status": "planned",
      "implemented": false,
      "technically_verified": false,
      "human_approved": false,
      "blocked": false,
      "issue_url": "https://github.com/jea27/Lut_generator/issues/68",
      "pr_url": "https://github.com/jea27/Lut_generator/pull/70",
      "evidence": [],
      "review": {
        "state": "pending",
        "context": null,
        "history": [],
        "latest": null
      },
      "review_steps": [
        "Esta capacidad todavía no tiene una entrega revisable."
      ],
      "checklist": [
        {
          "id": "behavior",
          "label": "El comportamiento descrito funciona en mi prueba."
        },
        {
          "id": "quality",
          "label": "He comparado el resultado y no encuentro un fallo bloqueante en este alcance."
        },
        {
          "id": "evidence",
          "label": "He comprobado versión, evidencias y limitaciones de la entrega."
        }
      ],
      "verification_scope": "Tests de main y evidencia versionada; no aceptación estética ni Windows limpio"
    },
    {
      "id": "halation",
      "title": "Halation",
      "group": "Futuro",
      "task": "COL-026",
      "acceptance": "Efecto espacial pendiente, independiente de LUT y controlable; posterior a beta.",
      "status": "planned",
      "implemented": false,
      "technically_verified": false,
      "human_approved": false,
      "blocked": false,
      "issue_url": "https://github.com/jea27/Lut_generator/issues/68",
      "pr_url": "https://github.com/jea27/Lut_generator/pull/70",
      "evidence": [],
      "review": {
        "state": "pending",
        "context": null,
        "history": [],
        "latest": null
      },
      "review_steps": [
        "Esta capacidad todavía no tiene una entrega revisable."
      ],
      "checklist": [
        {
          "id": "behavior",
          "label": "El comportamiento descrito funciona en mi prueba."
        },
        {
          "id": "quality",
          "label": "He comparado el resultado y no encuentro un fallo bloqueante en este alcance."
        },
        {
          "id": "evidence",
          "label": "He comprobado versión, evidencias y limitaciones de la entrega."
        }
      ],
      "verification_scope": "Tests de main y evidencia versionada; no aceptación estética ni Windows limpio"
    }
  ],
  "metrics": {
    "technical": {
      "passed": 8,
      "total": 8,
      "unknown": 0,
      "percent": 100
    },
    "human": {
      "passed": 0,
      "total": 8,
      "unknown": 0,
      "percent": 0
    }
  },
  "readiness": {
    "beta": {
      "checks": [
        {
          "id": "candidate",
          "title": "Candidato versionado y hash verificable",
          "passed": true,
          "issue_url": null
        },
        {
          "id": "clean-windows",
          "title": "Instalación en Windows limpio",
          "passed": false,
          "issue_url": null
        },
        {
          "id": "licenses",
          "title": "Derechos de redistribución y privacidad",
          "passed": false,
          "issue_url": "https://github.com/jea27/Lut_generator/issues/60"
        },
        {
          "id": "pilot",
          "title": "Piloto externo y soporte aceptados",
          "passed": false,
          "issue_url": "https://github.com/jea27/Lut_generator/issues/61"
        },
        {
          "id": "distribution",
          "title": "Autorización expresa de entrega",
          "passed": false,
          "issue_url": null
        }
      ],
      "metric": {
        "passed": 1,
        "total": 5,
        "unknown": 0,
        "percent": 20
      },
      "go": false
    },
    "commercial": {
      "checks": [
        {
          "id": "p0",
          "title": "Decisión humana P0",
          "passed": false,
          "issue_url": "https://github.com/jea27/Lut_generator/issues/19"
        },
        {
          "id": "licenses",
          "title": "Auditoría legal aceptada",
          "passed": false,
          "issue_url": "https://github.com/jea27/Lut_generator/issues/60"
        },
        {
          "id": "beta",
          "title": "Beta aceptada por usuarios",
          "passed": false,
          "issue_url": "https://github.com/jea27/Lut_generator/issues/61"
        },
        {
          "id": "launch",
          "title": "Lanzamiento y condiciones",
          "passed": false,
          "issue_url": "https://github.com/jea27/Lut_generator/issues/62"
        }
      ],
      "metric": {
        "passed": 0,
        "total": 4,
        "unknown": 0,
        "percent": 0
      },
      "go": false
    }
  },
  "pull_requests": [
    {
      "number": 79,
      "title": "[COL-044] Revisiones humanas individuales desde el dashboard",
      "state": "draft",
      "url": "https://github.com/jea27/Lut_generator/pull/79",
      "base": "main",
      "updated_at": "2026-10-31T10:00:53Z"
    },
    {
      "number": 70,
      "title": "[COL-026] Integrar beta2, Look Match y auditoría pendientes en main",
      "state": "merged",
      "url": "https://github.com/jea27/Lut_generator/pull/70",
      "base": "main",
      "updated_at": "2026-10-31T09:38:10Z"
    },
    {
      "number": 74,
      "title": "[COL-043] Centro de control automático del progreso real de Color Studio",
      "state": "merged",
      "url": "https://github.com/jea27/Lut_generator/pull/74",
      "base": "main",
      "updated_at": "2026-10-31T09:33:06Z"
    },
    {
      "number": 71,
      "title": "[COL-013] Estabilizar QA de beta0.3 y bloquear procedencia binaria no conciliada",
      "state": "merged",
      "url": "https://github.com/jea27/Lut_generator/pull/71",
      "base": "main",
      "updated_at": "2026-10-31T09:20:16Z"
    },
    {
      "number": 69,
      "title": "[COL-026] Look Match manual y candidato beta para QA externa",
      "state": "merged",
      "url": "https://github.com/jea27/Lut_generator/pull/69",
      "base": "codex/COL-042-preparacion-comercial",
      "updated_at": "2026-10-31T08:05:28Z"
    },
    {
      "number": 66,
      "title": "[COL-040] [COL-042] Landing local y preparación comercial de la beta",
      "state": "merged",
      "url": "https://github.com/jea27/Lut_generator/pull/66",
      "base": "codex/COL-037-beta-estabilidad",
      "updated_at": "2026-10-31T08:00:25Z"
    },
    {
      "number": 65,
      "title": "[COL-036] [COL-037] Beta Windows instalable y lotes persistentes",
      "state": "merged",
      "url": "https://github.com/jea27/Lut_generator/pull/65",
      "base": "main",
      "updated_at": "2026-10-31T08:00:10Z"
    },
    {
      "number": 63,
      "title": "[COL-005] Definir Look Match y acabado visual v1.0",
      "state": "merged",
      "url": "https://github.com/jea27/Lut_generator/pull/63",
      "base": "main",
      "updated_at": "2026-10-30T20:53:33Z"
    },
    {
      "number": 64,
      "title": "[COL-006] Diagnosticar duplicado #56 y deduplicación de avisos",
      "state": "merged",
      "url": "https://github.com/jea27/Lut_generator/pull/64",
      "base": "main",
      "updated_at": "2026-10-30T20:53:21Z"
    },
    {
      "number": 53,
      "title": "[COL-015] Entregar Color Studio funcional para Windows",
      "state": "merged",
      "url": "https://github.com/jea27/Lut_generator/pull/53",
      "base": "main",
      "updated_at": "2026-10-30T20:33:28Z"
    },
    {
      "number": 52,
      "title": "[COL-007] Implementar motor clásico local y exportaciones MVP",
      "state": "merged",
      "url": "https://github.com/jea27/Lut_generator/pull/52",
      "base": "main",
      "updated_at": "2026-10-30T20:32:03Z"
    },
    {
      "number": 38,
      "title": "[COL-006] Registrar enlace publicado, pruebas móviles y recuperación",
      "state": "merged",
      "url": "https://github.com/jea27/Lut_generator/pull/38",
      "base": "main",
      "updated_at": "2026-10-30T20:31:35Z"
    }
  ],
  "ci": [
    {
      "name": "Sincronizar roadmap",
      "branch": "codex/COL-044-human-review",
      "sha": "015fc895f56e684daff7527290123e2233a7d30c",
      "status": "queued",
      "conclusion": null,
      "url": "https://github.com/jea27/Lut_generator/actions/runs/41191386973",
      "updated_at": "2026-10-31T10:06:28Z"
    },
    {
      "name": "Sincronizar roadmap",
      "branch": "main",
      "sha": "448a1015c1f0b424a9ed85a50a52a542d7e03acd",
      "status": "completed",
      "conclusion": "success",
      "url": "https://github.com/jea27/Lut_generator/actions/runs/41191053395",
      "updated_at": "2026-10-31T10:02:15Z"
    },
    {
      "name": "Sincronizar roadmap",
      "branch": "codex/COL-006-product-dashboard",
      "sha": "5733a3b93fecc80c447e847a856fba5681b560e2",
      "status": "completed",
      "conclusion": "success",
      "url": "https://github.com/jea27/Lut_generator/actions/runs/41189158382",
      "updated_at": "2026-10-31T09:33:44Z"
    },
    {
      "name": "Publicar roadmap",
      "branch": "codex/COL-044-human-review",
      "sha": "015fc895f56e684daff7527290123e2233a7d30c",
      "status": "completed",
      "conclusion": "success",
      "url": "https://github.com/jea27/Lut_generator/actions/runs/41190994499",
      "updated_at": "2026-10-31T10:01:20Z"
    },
    {
      "name": "Publicar roadmap",
      "branch": "main",
      "sha": "448a1015c1f0b424a9ed85a50a52a542d7e03acd",
      "status": "completed",
      "conclusion": "cancelled",
      "url": "https://github.com/jea27/Lut_generator/actions/runs/41189148832",
      "updated_at": "2026-10-31T09:33:44Z"
    },
    {
      "name": "Publicar roadmap",
      "branch": "codex/COL-006-product-dashboard",
      "sha": "5733a3b93fecc80c447e847a856fba5681b560e2",
      "status": "completed",
      "conclusion": "success",
      "url": "https://github.com/jea27/Lut_generator/actions/runs/41189097370",
      "updated_at": "2026-10-31T09:32:51Z"
    },
    {
      "name": "Publicar roadmap",
      "branch": "codex/COL-013-estabilizacion-beta3",
      "sha": "e20c34b9e4cb06f369c5a693581389d977dda19f",
      "status": "completed",
      "conclusion": "success",
      "url": "https://github.com/jea27/Lut_generator/actions/runs/41187873807",
      "updated_at": "2026-10-31T09:14:34Z"
    },
    {
      "name": "Validar MVP local",
      "branch": "codex/COL-044-human-review",
      "sha": "015fc895f56e684daff7527290123e2233a7d30c",
      "status": "completed",
      "conclusion": "success",
      "url": "https://github.com/jea27/Lut_generator/actions/runs/41190994497",
      "updated_at": "2026-10-31T10:01:42Z"
    },
    {
      "name": "Compilar Color Studio",
      "branch": "codex/COL-044-human-review",
      "sha": "015fc895f56e684daff7527290123e2233a7d30c",
      "status": "completed",
      "conclusion": "success",
      "url": "https://github.com/jea27/Lut_generator/actions/runs/41190994486",
      "updated_at": "2026-10-31T10:01:37Z"
    },
    {
      "name": "Compilar Color Studio",
      "branch": "main",
      "sha": "448a1015c1f0b424a9ed85a50a52a542d7e03acd",
      "status": "completed",
      "conclusion": "success",
      "url": "https://github.com/jea27/Lut_generator/actions/runs/41189148771",
      "updated_at": "2026-10-31T09:33:41Z"
    },
    {
      "name": "Validar MVP local",
      "branch": "main",
      "sha": "448a1015c1f0b424a9ed85a50a52a542d7e03acd",
      "status": "completed",
      "conclusion": "success",
      "url": "https://github.com/jea27/Lut_generator/actions/runs/41189148708",
      "updated_at": "2026-10-31T09:33:49Z"
    },
    {
      "name": "Compilar Color Studio",
      "branch": "codex/COL-006-product-dashboard",
      "sha": "5733a3b93fecc80c447e847a856fba5681b560e2",
      "status": "completed",
      "conclusion": "success",
      "url": "https://github.com/jea27/Lut_generator/actions/runs/41189083924",
      "updated_at": "2026-10-31T09:32:53Z"
    }
  ],
  "installer_build": null,
  "installer_artifacts": [],
  "human_requests": [
    {
      "number": 15,
      "title": "[LUMAFORGE] ACCIÓN REQUERIDA — Aceptar o corregir documentación COL-005",
      "url": "https://github.com/jea27/Lut_generator/issues/15",
      "updated_at": "2026-10-31T09:51:08Z"
    },
    {
      "number": 21,
      "title": "[LUMAFORGE] ACCIÓN REQUERIDA — Revisar [COL-006] PR #20",
      "url": "https://github.com/jea27/Lut_generator/issues/21",
      "updated_at": "2026-10-31T09:51:02Z"
    },
    {
      "number": 75,
      "title": "[LUMAFORGE] ACCIÓN REQUERIDA — Revisar [COL-043] PR #74",
      "url": "https://github.com/jea27/Lut_generator/issues/75",
      "updated_at": "2026-10-31T09:49:09Z"
    },
    {
      "number": 73,
      "title": "[LUMAFORGE] ACCIÓN REQUERIDA — Coordinar worktree de dashboard",
      "url": "https://github.com/jea27/Lut_generator/issues/73",
      "updated_at": "2026-10-31T09:42:25Z"
    },
    {
      "number": 67,
      "title": "[LUMAFORGE] ACCIÓN REQUERIDA — Resolver procedencia del runtime y ejecutar QA limpia",
      "url": "https://github.com/jea27/Lut_generator/issues/67",
      "updated_at": "2026-10-31T08:51:10Z"
    },
    {
      "number": 56,
      "title": "[LUMAFORGE] ACCIÓN REQUERIDA — Revisar [COL-005] PR #55",
      "url": "https://github.com/jea27/Lut_generator/issues/56",
      "updated_at": "2026-10-30T20:21:44Z"
    },
    {
      "number": 54,
      "title": "[LUMAFORGE] ACCIÓN REQUERIDA — Probar y revisar LumaForge MVP local",
      "url": "https://github.com/jea27/Lut_generator/issues/54",
      "updated_at": "2026-10-30T20:06:28Z"
    },
    {
      "number": 29,
      "title": "[LUMAFORGE] ACCIÓN REQUERIDA — Publicar formulario y probar JSON en iPhone",
      "url": "https://github.com/jea27/Lut_generator/issues/29",
      "updated_at": "2026-10-30T19:27:17Z"
    },
    {
      "number": 27,
      "title": "[LUMAFORGE] ACCIÓN REQUERIDA — Revisar [COL-003] PR #26",
      "url": "https://github.com/jea27/Lut_generator/issues/27",
      "updated_at": "2026-10-30T16:29:41Z"
    },
    {
      "number": 25,
      "title": "[LUMAFORGE] ACCIÓN REQUERIDA — Revisar [COL-002] PR #23",
      "url": "https://github.com/jea27/Lut_generator/issues/25",
      "updated_at": "2026-10-30T16:22:16Z"
    },
    {
      "number": 24,
      "title": "[LUMAFORGE] ACCIÓN REQUERIDA — Revisar [COL-004] PR #22",
      "url": "https://github.com/jea27/Lut_generator/issues/24",
      "updated_at": "2026-10-30T16:22:08Z"
    }
  ],
  "operations": [
    {
      "id": "COL-043",
      "title": "Dashboard real de producto y sincronización GitHub",
      "status": "review",
      "excluded_from_product_metrics": true,
      "issue_url": "https://github.com/jea27/Lut_generator/issues/72",
      "pr_url": "https://github.com/jea27/Lut_generator/pull/74"
    }
  ],
  "privacy": "Solo metadatos públicos permitidos; no cuerpos, logs, fotos, datos de participantes o rutas locales.",
  "reviews_active": false,
  "review_demo": {
    "id": "review-demo",
    "title": "Demostración de revisión (sintética)",
    "task": "COL-044",
    "acceptance": "Comprobar únicamente la infraestructura de revisión; no aprueba Color Studio.",
    "demo": true,
    "implemented": true,
    "human_approved": false,
    "technically_verified": true,
    "review": {
      "state": "changes_requested",
      "context": {
        "commit": "015fc895f56e684daff7527290123e2233a7d30c",
        "version": "0.3.0-beta.2",
        "revision": "f6a33b34aa383b6eb03ee384be9bce77c9b8161b0965350cf7d55560a59c3708"
      },
      "history": [
        {
          "feature": "review-demo",
          "revision": "f6a33b34aa383b6eb03ee384be9bce77c9b8161b0965350cf7d55560a59c3708",
          "commit": "015fc895f56e684daff7527290123e2233a7d30c",
          "version": "0.3.0-beta.2",
          "decision": "approve",
          "checklist": [
            "demo-visible",
            "no-product"
          ],
          "reviewer": "jea27",
          "at": "2026-10-31T10:01:36Z",
          "comment_id": 6541989840,
          "notes_present": false,
          "demo": true,
          "source_valid": true,
          "url": "https://github.com/jea27/Lut_generator/issues/77#issuecomment-6541989840"
        },
        {
          "feature": "review-demo",
          "revision": "f6a33b34aa383b6eb03ee384be9bce77c9b8161b0965350cf7d55560a59c3708",
          "commit": "015fc895f56e684daff7527290123e2233a7d30c",
          "version": "0.3.0-beta.2",
          "decision": "changes",
          "checklist": [],
          "reviewer": "jea27",
          "at": "2026-10-31T10:05:25Z",
          "comment_id": 6542024460,
          "notes_present": true,
          "demo": true,
          "source_valid": true,
          "url": "https://github.com/jea27/Lut_generator/issues/77#issuecomment-6542024460"
        }
      ],
      "latest": {
        "feature": "review-demo",
        "revision": "f6a33b34aa383b6eb03ee384be9bce77c9b8161b0965350cf7d55560a59c3708",
        "commit": "015fc895f56e684daff7527290123e2233a7d30c",
        "version": "0.3.0-beta.2",
        "decision": "changes",
        "checklist": [],
        "reviewer": "jea27",
        "at": "2026-10-31T10:05:25Z",
        "comment_id": 6542024460,
        "notes_present": true,
        "demo": true,
        "source_valid": true,
        "url": "https://github.com/jea27/Lut_generator/issues/77#issuecomment-6542024460"
      }
    },
    "review_steps": [
      "Comprobar que esta tarjeta está marcada como demostración sin impacto en producto.",
      "Completar checklist y probar el comentario de aprobación o corrección en Issue77."
    ],
    "checklist": [
      {
        "id": "demo-visible",
        "label": "La tarjeta indica que es una demostración sintética."
      },
      {
        "id": "no-product",
        "label": "Confirmo que no estoy aprobando una capacidad real."
      }
    ],
    "issue_url": "https://github.com/jea27/Lut_generator/issues/77",
    "evidence": [],
    "pr_url": null
  }
};
