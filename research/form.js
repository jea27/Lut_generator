'use strict';
// Browser-local answers. Static hosting only; export is initiated by the participant.
const VERSION = 'LF-P0-FORM-2026-10-30-v1';
const QUESTIONS = [
  'Q1. Tipo de proyectos, segmento A/B/C/D, sistema operativo y autonomía de compra (sin nombres ni empresa).',
  'Q2. Último caso real de adaptar una referencia o igualar looks. ¿Cuándo ocurrió? Si no existe, indícalo.',
  'Q3. Pasos y herramientas que utilizaste en ese caso. ¿Moviste un look entre editores? ¿Cómo?',
  'Q4. En los últimos 30 días, ¿cuántas ocasiones de este trabajo? Distingue proyectos de imágenes.',
  'Q5. Tiempo de corrección de look en el último caso y otro reciente. ¿Medido o estimado? No incluyas todo el proyecto.',
  'Q6. ¿Qué resolvió tu solución actual y qué quedó pendiente? ¿Hubo consecuencias o repetición?',
  'Q7. ¿Qué dos cosas pesan más al elegir una herramienta para ese trabajo?',
  'Q8. ¿Qué has probado o pagado en 12 meses? Importe opcional, periodicidad, motivo para mantenerlo o abandonarlo. Restricciones reales de conexión/equipo/formatos.',
  'Q9. ¿Qué entiendes que resolvería el concepto? ¿Dónde sería útil o inútil en tu último caso?',
  'Q10. ¿Qué seguirías haciendo con tu solución actual? ¿Qué tendría que demostrar para cambiar?',
  'Q11. Antes de mostrar un precio: ¿qué importe total, si alguno, considerarías razonable? ¿Preferirías no pagar o mantener tu solución?',
  'Q12. A 49 € de pago único: ¿comprar si la prueba cumple tus criterios, mantener solución actual/gratuita, otra solución de pago, no decidir o prefieres no responder? ¿Por qué?',
  'Q13. ¿Qué condición concreta impediría comprar? No cuentes funciones fuera del alcance como incluidas.',
  'Q14. ¿Cómo afectaría pago único frente a suscripción? ¿Qué prestación recurrente justificaría pagar periódicamente?',
  'Q15. ¿Qué paso concreto darías, si alguno, y qué tendrías que ver antes? Es intención, no compra. ¿Quieres retirar alguna nota?'
];

function makeResponse(code, consent, answers, timestamps, uuid, now) {
  if (!/^R(?!000)[0-9]{3}$/.test(code) || consent !== true) throw new Error('Código R001–R999 y consentimiento requeridos');
  if (!Array.isArray(answers) || answers.length !== 15 || answers.some(a => typeof a !== 'string' || a.length > 2000)) {
    throw new Error('Quince respuestas textuales de máximo 2000 caracteres');
  }
  if (!Array.isArray(timestamps) || timestamps.length !== 3 || timestamps.some(t => !Number.isFinite(Date.parse(t))) ||
      timestamps.some((t, i) => i > 0 && Date.parse(t) < Date.parse(timestamps[i-1]))) {
    throw new Error('Secuencia de etapas inválida');
  }
  if (!/^[0-9a-f-]{36}$/i.test(uuid) || !Number.isFinite(Date.parse(now)) || Date.parse(now) < Date.parse(timestamps[2])) {
    throw new Error('Identificador o fecha inválidos');
  }
  return {version: VERSION, response_id: uuid, participant_code: code,
    evidence_type: 'self_report_form', status: 'submitted_unverified', notes_consent: true,
    price_eur_shown: 49, completed_utc: now, stage_completed_utc: [...timestamps],
    answers: answers.map((answer, i) => ({question: 'Q' + (i+1), answer: answer.trim(),
      disposition: answer.trim() ? 'answered' : 'omitted'}))};
}

function participantCodeFromHash(hash) {
  return /^#R(?!000)[0-9]{3}$/.test(hash) ? hash.slice(1) : '';
}

function canShareFile(navigatorObject, file) {
  try {
    return typeof navigatorObject.share === 'function' && typeof navigatorObject.canShare === 'function'
      && navigatorObject.canShare({files: [file]}) === true;
  } catch { return false; }
}

async function shareResponse(navigatorObject, file) {
  if (!canShareFile(navigatorObject, file)) return 'unavailable';
  try { await navigatorObject.share({files: [file]}); return 'handed_to_share_ui'; }
  catch (error) { return error.name === 'AbortError' ? 'cancelled' : 'failed'; }
}

if (typeof module !== 'undefined') module.exports = {VERSION, QUESTIONS, makeResponse, participantCodeFromHash, canShareFile, shareResponse};
if (typeof document !== 'undefined') {
  let stage = 0;
  const answers = [], timestamps = [];
  const groups = [[0, 8], [8, 11], [11, 15]];
  const form = document.querySelector('form');
  const heading = document.querySelector('#stage');
  const fields = document.querySelector('#questions');
  const notice = document.querySelector('#notice');
  const button = document.querySelector('#continue');
  const codeField = document.querySelector('#code');
  codeField.value = participantCodeFromHash(window.location.hash);
  let exportedFile = null;
  function download() {
    if (!exportedFile) return;
    const url = URL.createObjectURL(exportedFile);
    const link = document.createElement('a'); link.href = url; link.download = exportedFile.name;
    document.body.append(link); link.click(); link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 60000);
    notice.textContent = 'Descarga solicitada. Comprueba el archivo en Archivos/Descargas. No se ha enviado a ningún destinatario.';
  }
  document.querySelector('#download').addEventListener('click', download);
  document.querySelector('#share').addEventListener('click', async () => {
    const result = await shareResponse(navigator, exportedFile);
    notice.textContent = {
      unavailable: 'Este navegador no permite compartir el archivo. Usa Descargar JSON.',
      handed_to_share_ui: 'Archivo entregado al menú de compartir. Comprueba el destinatario y la recepción por el canal acordado; no podemos verificar la entrega.',
      cancelled: 'Compartir cancelado. Tu respuesta sigue disponible para descargar; no se confirma ningún envío.',
      failed: 'No se pudo compartir. Tu respuesta sigue disponible: usa Descargar JSON.'
    }[result];
  });
  function render() {
    heading.textContent = ['1 de 3 · Tu trabajo real', '2 de 3 · Concepto e importe espontáneo', '3 de 3 · Escenario de precio'][stage];
    document.querySelector('#concept').hidden = stage !== 1;
    document.querySelector('#price').hidden = stage !== 2;
    fields.replaceChildren();
    for (let q = groups[stage][0]; q < groups[stage][1]; q++) {
      const label = document.createElement('label');
      label.textContent = QUESTIONS[q];
      const input = document.createElement('textarea');
      input.name = 'Q' + (q+1); input.maxLength = 2000; input.rows = 3;
      label.append(input); fields.append(label);
    }
    button.textContent = stage === 2 ? 'Preparar JSON sin enviar' : 'Guardar esta etapa y continuar';
  }
  form.addEventListener('submit', event => {
    event.preventDefault();
    if (exportedFile) return;
    const code = document.querySelector('#code').value;
    if (!/^R(?!000)[0-9]{3}$/.test(code) || !document.querySelector('#consent').checked) {
      notice.textContent = 'Introduce un código R001–R999 y acepta notas anonimizadas para continuar.'; return;
    }
    for (let q = groups[stage][0]; q < groups[stage][1]; q++) answers[q] = form.elements['Q' + (q+1)].value;
    timestamps[stage] = new Date().toISOString();
    document.querySelector('#code').readOnly = true;
    document.querySelector('#consent').disabled = true;
    if (stage < 2) { stage++; render(); window.scrollTo(0, 0); return; }
    try {
      const payload = makeResponse(code, true, answers, timestamps, crypto.randomUUID(), new Date().toISOString());
      const json = JSON.stringify(payload, null, 2);
      exportedFile = new File([json], code + '-respuesta.json', {type:'application/json'});
      document.querySelector('#preview').textContent = json;
      document.querySelector('#export-options').hidden = false;
      document.querySelector('#questions').hidden = true;
      document.querySelector('#share').hidden = !canShareFile(navigator, exportedFile);
      button.hidden = true;
      notice.textContent = 'Archivo preparado localmente. Nada enviado. Elige descargar o compartir y comprueba que no contiene identificadores personales.';
    } catch (error) { notice.textContent = error.message; }
  });
  render();
}
