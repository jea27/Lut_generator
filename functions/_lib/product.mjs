import { HttpError } from './security.mjs';

export const PRODUCT_SNAPSHOT_URL = 'https://jea27.github.io/Lut_generator/data/product.json';
const SNAPSHOT_MAX_BYTES = 2 * 1024 * 1024;
const SNAPSHOT_MAX_AGE_MS = 60 * 60 * 1000;
const REVIEW_PREFIX = 'LUMAFORGE_REVIEW_V1\n```json\n';
const REVIEW_ISSUES = Object.freeze({
  'color-match': 43, 'manual-look': 68, glow: 68, diffusion: 68, fade: 68,
  presets: 50, batches: 58, 'lut-export': 44, 'image-export': 51, recipe: 50,
  windows: 57, adobe: 59, resolve: 59, 'automatic-look': 68, halation: 68,
  creator: 81, 'pro-workspace': 82, 'shot-planner': 83,
});

function isRecord(value) {
  return Boolean(value && typeof value === 'object' && !Array.isArray(value));
}

export function validateSnapshotShape(snapshot) {
  if (!isRecord(snapshot) || snapshot.schema_version !== 1 || !isRecord(snapshot.sync)) return false;
  if (!/^[a-f0-9]{40}$/.test(snapshot.sync.main_sha || '') || !Number.isFinite(Date.parse(snapshot.sync.observed_at || ''))) return false;
  return Array.isArray(snapshot.features) && typeof snapshot.reviews_active === 'boolean';
}

export async function loadProductSnapshot(fetchImpl = fetch, now = Date.now()) {
  const url = new URL(PRODUCT_SNAPSHOT_URL);
  url.searchParams.set('_', String(now));
  let response;
  try {
    response = await fetchImpl(url, {
      headers: { Accept: 'application/json' },
      cache: 'no-store',
      redirect: 'error',
      signal: AbortSignal.timeout(10000),
    });
  } catch {
    throw new HttpError(503, 'product_snapshot_unavailable');
  }
  if (!response.ok || response.headers.get('Content-Type')?.toLowerCase().split(';')[0] !== 'application/json') {
    throw new HttpError(503, 'product_snapshot_unavailable');
  }
  const declared = Number(response.headers.get('Content-Length'));
  if (Number.isFinite(declared) && declared > SNAPSHOT_MAX_BYTES) throw new HttpError(503, 'product_snapshot_unavailable');
  let raw;
  try {
    raw = await response.text();
    if (new TextEncoder().encode(raw).byteLength > SNAPSHOT_MAX_BYTES) throw new Error('too_large');
  } catch {
    throw new HttpError(503, 'product_snapshot_unavailable');
  }
  let snapshot;
  try {
    snapshot = JSON.parse(raw);
  } catch {
    throw new HttpError(503, 'product_snapshot_unavailable');
  }
  if (!validateSnapshotShape(snapshot)) throw new HttpError(503, 'product_snapshot_unavailable');
  const observedAt = Date.parse(snapshot.sync.observed_at);
  if (observedAt > now + 5 * 60 * 1000 || now - observedAt > SNAPSHOT_MAX_AGE_MS) {
    throw new HttpError(503, 'product_snapshot_stale');
  }
  if (!snapshot.reviews_active) throw new HttpError(503, 'review_workflow_unavailable');
  return snapshot;
}

function issueNumberFromFeature(feature) {
  const issueUrl = feature?.issue_url;
  if (typeof issueUrl !== 'string') return null;
  const match = issueUrl.match(/^https:\/\/github\.com\/jea27\/Lut_generator\/issues\/([1-9][0-9]*)$/);
  if (!match) return null;
  const issue = Number(match[1]);
  if (feature.id === 'review-demo') return issue === 77 ? issue : null;
  return Object.hasOwn(REVIEW_ISSUES, feature.id) && REVIEW_ISSUES[feature.id] === issue ? issue : null;
}

function currentContext(feature) {
  const context = feature?.review?.context;
  if (!isRecord(context) || !/^[a-f0-9]{40}$/.test(context.commit || '') || !/^[a-f0-9]{64}$/.test(context.revision || '') || typeof context.version !== 'string' || !context.version || context.version.length > 80) return null;
  return context;
}

function strictPayloadKeys(body) {
  const keys = Object.keys(body || {}).sort();
  return keys.join(',') === ['checklist', 'commit', 'decision', 'feature', 'notes', 'revision', 'version'].sort().join(',');
}

export function validateDecision(body, pathFeatureId, snapshot, { enableDemo = false } = {}) {
  if (!isRecord(body) || !strictPayloadKeys(body)) throw new HttpError(400, 'invalid_decision');
  if (typeof pathFeatureId !== 'string' || body.feature !== pathFeatureId || !/^[a-z0-9][a-z0-9-]{0,63}$/.test(body.feature)) throw new HttpError(400, 'invalid_feature');
  if (!['approve', 'changes'].includes(body.decision)) throw new HttpError(400, 'invalid_decision');
  if (typeof body.revision !== 'string' || !/^[a-f0-9]{64}$/.test(body.revision) || typeof body.commit !== 'string' || !/^[a-f0-9]{40}$/.test(body.commit)) throw new HttpError(400, 'invalid_revision');
  if (typeof body.version !== 'string' || body.version.length < 1 || body.version.length > 80 || /[\u0000-\u001f\u007f]/.test(body.version)) throw new HttpError(400, 'invalid_version');
  if (!Array.isArray(body.checklist) || body.checklist.length > 40 || body.checklist.some(id => typeof id !== 'string' || !/^[a-z0-9][a-z0-9-]{0,63}$/.test(id)) || new Set(body.checklist).size !== body.checklist.length) throw new HttpError(400, 'invalid_checklist');
  if (typeof body.notes !== 'string' || body.notes.length > 2000 || /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/.test(body.notes)) throw new HttpError(400, 'invalid_notes');
  if (body.decision === 'changes' && !body.notes.trim()) throw new HttpError(422, 'notes_required');
  if (!snapshot.reviews_active) throw new HttpError(503, 'review_workflow_unavailable');

  let feature;
  let demo = false;
  if (body.feature === 'review-demo') {
    feature = snapshot.review_demo;
    demo = true;
    if (!enableDemo || !feature?.demo || feature.id !== 'review-demo' || issueNumberFromFeature(feature) !== 77) throw new HttpError(403, 'demo_disabled');
  } else {
    feature = snapshot.features.find(item => item?.id === body.feature);
    if (!feature || feature.demo || feature.human_approved === true || feature.review?.state === 'approved') throw new HttpError(409, 'feature_not_pending');
  }

  const issue = issueNumberFromFeature(feature);
  const context = currentContext(feature);
  if (!issue || !context) throw new HttpError(503, 'review_context_unavailable');
  if (body.commit !== context.commit || body.revision !== context.revision || body.version !== context.version) throw new HttpError(409, 'review_version_changed');
  const ids = Array.isArray(feature.checklist) ? feature.checklist.map(item => item?.id) : [];
  if (!ids.length || ids.some(id => typeof id !== 'string' || !/^[a-z0-9][a-z0-9-]{0,63}$/.test(id)) || new Set(ids).size !== ids.length) throw new HttpError(503, 'review_checklist_unavailable');
  if (body.checklist.some(id => !ids.includes(id))) throw new HttpError(400, 'invalid_checklist');
  if (body.decision === 'approve' && (body.checklist.length !== ids.length || ids.some(id => !body.checklist.includes(id)))) throw new HttpError(422, 'checklist_incomplete');

  return { feature, issue, demo, context, checklistIds: ids };
}

export function serializeReviewComment(body) {
  const payload = {
    feature: body.feature,
    revision: body.revision,
    commit: body.commit,
    version: body.version,
    decision: body.decision,
    checklist: body.checklist,
    notes: body.notes,
  };
  return `${REVIEW_PREFIX}${JSON.stringify(payload, null, 2)}\n\`\`\``;
}

export function canonicalIssueCommentUrl(issue, commentId) {
  if (!Number.isSafeInteger(issue) || issue < 1 || !Number.isSafeInteger(commentId) || commentId < 1) throw new Error('invalid_comment_reference');
  return `https://github.com/jea27/Lut_generator/issues/${issue}#issuecomment-${commentId}`;
}

export function issueNumberForTesting(feature) {
  return issueNumberFromFeature(feature);
}
