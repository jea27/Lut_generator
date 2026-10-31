window.INITIAL_PRODUCT = {
  "schema_version": 1,
  "product": "Color Studio",
  "sync": {
    "status": "complete",
    "observed_at": "2026-10-31T09:30:32.388771Z",
    "main_sha": "5b6a910cfa5f67e060a00337d3db39b2404d81c7"
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
      "number": 74,
      "title": "[COL-043] Centro de control automático del progreso real de Color Studio",
      "state": "draft",
      "url": "https://github.com/jea27/Lut_generator/pull/74",
      "base": "main",
      "updated_at": "2026-10-31T09:23:27Z"
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
      "number": 70,
      "title": "[COL-026] Integrar beta2, Look Match y auditoría pendientes en main",
      "state": "merged",
      "url": "https://github.com/jea27/Lut_generator/pull/70",
      "base": "main",
      "updated_at": "2026-10-31T08:51:17Z"
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
    },
    {
      "number": 37,
      "title": "[COL-003] Preparar experimentos y ejecutar controles CC0",
      "state": "merged",
      "url": "https://github.com/jea27/Lut_generator/pull/37",
      "base": "main",
      "updated_at": "2026-10-30T20:31:20Z"
    }
  ],
  "ci": [
    {
      "name": "Sincronizar roadmap",
      "branch": "main",
      "sha": "5b6a910cfa5f67e060a00337d3db39b2404d81c7",
      "status": "completed",
      "conclusion": "success",
      "url": "https://github.com/jea27/Lut_generator/actions/runs/41188660847",
      "updated_at": "2026-10-31T09:26:32Z"
    },
    {
      "name": "Publicar roadmap",
      "branch": "main",
      "sha": "5b6a910cfa5f67e060a00337d3db39b2404d81c7",
      "status": "completed",
      "conclusion": "success",
      "url": "https://github.com/jea27/Lut_generator/actions/runs/41188285576",
      "updated_at": "2026-10-31T09:20:57Z"
    },
    {
      "name": "Publicar roadmap",
      "branch": "codex/COL-006-product-dashboard",
      "sha": "d3b8d92eaff3413f055b6d4aab2b2b0b31e24cc9",
      "status": "completed",
      "conclusion": "success",
      "url": "https://github.com/jea27/Lut_generator/actions/runs/41188254963",
      "updated_at": "2026-10-31T09:20:16Z"
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
      "name": "Publicar roadmap",
      "branch": "codex/COL-026-integracion-beta2",
      "sha": "4920cf0e38bac165147158d4bd6e4c09ceedb913",
      "status": "completed",
      "conclusion": "success",
      "url": "https://github.com/jea27/Lut_generator/actions/runs/41184186206",
      "updated_at": "2026-10-31T08:20:26Z"
    },
    {
      "name": "Compilar Color Studio",
      "branch": "main",
      "sha": "5b6a910cfa5f67e060a00337d3db39b2404d81c7",
      "status": "completed",
      "conclusion": "success",
      "url": "https://github.com/jea27/Lut_generator/actions/runs/41188285564",
      "updated_at": "2026-10-31T09:21:03Z"
    },
    {
      "name": "Validar MVP local",
      "branch": "main",
      "sha": "5b6a910cfa5f67e060a00337d3db39b2404d81c7",
      "status": "completed",
      "conclusion": "success",
      "url": "https://github.com/jea27/Lut_generator/actions/runs/41188285547",
      "updated_at": "2026-10-31T09:21:06Z"
    },
    {
      "name": "Compilar Color Studio",
      "branch": "codex/COL-006-product-dashboard",
      "sha": "d3b8d92eaff3413f055b6d4aab2b2b0b31e24cc9",
      "status": "completed",
      "conclusion": "success",
      "url": "https://github.com/jea27/Lut_generator/actions/runs/41188254955",
      "updated_at": "2026-10-31T09:20:33Z"
    },
    {
      "name": "Validar MVP local",
      "branch": "codex/COL-006-product-dashboard",
      "sha": "d3b8d92eaff3413f055b6d4aab2b2b0b31e24cc9",
      "status": "completed",
      "conclusion": "success",
      "url": "https://github.com/jea27/Lut_generator/actions/runs/41188254939",
      "updated_at": "2026-10-31T09:20:40Z"
    },
    {
      "name": "Validar MVP local",
      "branch": "codex/COL-013-estabilizacion-beta3",
      "sha": "e20c34b9e4cb06f369c5a693581389d977dda19f",
      "status": "completed",
      "conclusion": "success",
      "url": "https://github.com/jea27/Lut_generator/actions/runs/41187873868",
      "updated_at": "2026-10-31T09:15:04Z"
    },
    {
      "name": "Compilar Color Studio",
      "branch": "codex/COL-013-estabilizacion-beta3",
      "sha": "e20c34b9e4cb06f369c5a693581389d977dda19f",
      "status": "completed",
      "conclusion": "success",
      "url": "https://github.com/jea27/Lut_generator/actions/runs/41187873803",
      "updated_at": "2026-10-31T09:15:02Z"
    },
    {
      "name": "Compilar Color Studio",
      "branch": "codex/COL-026-integracion-beta2",
      "sha": "4920cf0e38bac165147158d4bd6e4c09ceedb913",
      "status": "completed",
      "conclusion": "success",
      "url": "https://github.com/jea27/Lut_generator/actions/runs/41184186164",
      "updated_at": "2026-10-31T08:21:07Z"
    }
  ],
  "installer_build": null,
  "installer_artifacts": [],
  "human_requests": [
    {
      "number": 73,
      "title": "[LUMAFORGE] ACCIÓN REQUERIDA — Coordinar worktree de dashboard",
      "url": "https://github.com/jea27/Lut_generator/issues/73",
      "updated_at": "2026-10-31T09:28:57Z"
    },
    {
      "number": 67,
      "title": "[LUMAFORGE] ACCIÓN REQUERIDA — Resolver procedencia del runtime y ejecutar QA limpia",
      "url": "https://github.com/jea27/Lut_generator/issues/67",
      "updated_at": "2026-10-31T08:51:10Z"
    },
    {
      "number": 21,
      "title": "[LUMAFORGE] ACCIÓN REQUERIDA — Revisar [COL-006] PR #20",
      "url": "https://github.com/jea27/Lut_generator/issues/21",
      "updated_at": "2026-10-30T20:51:01Z"
    },
    {
      "number": 15,
      "title": "[LUMAFORGE] ACCIÓN REQUERIDA — Aceptar o corregir documentación COL-005",
      "url": "https://github.com/jea27/Lut_generator/issues/15",
      "updated_at": "2026-10-30T20:50:59Z"
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
      "number": 3,
      "title": "[COL-000] Prueba real de aviso a GitHub Mobile",
      "url": "https://github.com/jea27/Lut_generator/issues/3",
      "updated_at": "2026-10-30T19:24:54Z"
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
    },
    {
      "number": 12,
      "title": "[COL-001] Revisión humana de PR #11",
      "url": "https://github.com/jea27/Lut_generator/issues/12",
      "updated_at": "2026-10-30T15:33:29Z"
    },
    {
      "number": 10,
      "title": "[COL-001] Revisión humana de PR #9",
      "url": "https://github.com/jea27/Lut_generator/issues/10",
      "updated_at": "2026-10-30T15:30:43Z"
    },
    {
      "number": 8,
      "title": "[COL-001] Revisión humana de PR #7",
      "url": "https://github.com/jea27/Lut_generator/issues/8",
      "updated_at": "2026-10-30T15:28:26Z"
    },
    {
      "number": 5,
      "title": "[COL-001] Revisión humana de PR #4",
      "url": "https://github.com/jea27/Lut_generator/issues/5",
      "updated_at": "2026-10-30T15:22:28Z"
    }
  ],
  "operations": [
    {
      "id": "COL-043",
      "title": "Dashboard real de producto y sincronización GitHub",
      "status": "progress",
      "excluded_from_product_metrics": true,
      "issue_url": "https://github.com/jea27/Lut_generator/issues/72",
      "pr_url": "https://github.com/jea27/Lut_generator/pull/74"
    }
  ],
  "privacy": "Solo metadatos públicos permitidos; no cuerpos, logs, fotos, datos de participantes o rutas locales."
};
