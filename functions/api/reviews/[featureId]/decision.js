import { createIssueComment, findExistingComment, GitHubError, verifyAuthorizedUser } from '../../../_lib/github.mjs';
import { canonicalIssueCommentUrl, loadProductSnapshot, serializeReviewComment, validateDecision } from '../../../_lib/product.mjs';
import { exactOrigin, HttpError, jsonResponse, matchesCsrf, readJson, sha256 } from '../../../_lib/security.mjs';
import { accessTokenFor, allowRate, getSession, validateConfig } from '../../../_lib/session.mjs';

function idempotencyKey(request) {
  const key = request.headers.get('Idempotency-Key');
  return typeof key === 'string' && /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(key) ? key.toLowerCase() : null;
}

function responseFor(row) {
  if (row.status === 'sent') {
    return jsonResponse(200, {
      status: 'submitted',
      feature: row.feature_id,
      decision: row.decision,
      comment: { id: row.comment_id, url: row.comment_url },
      dashboardSync: 'pending',
    });
  }
  return jsonResponse(202, { status: 'processing', feature: row.feature_id, decision: row.decision }, { 'Retry-After': '2' });
}

async function reserve(db, fields) {
  await db.prepare(`
    INSERT OR IGNORE INTO review_submissions
      (payload_hash, idempotency_hash, feature_id, issue_number, revision, decision, status, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, 'reserved', ?, ?)
  `).bind(fields.payloadHash, fields.idempotencyHash, fields.featureId, fields.issue, fields.revision,
    fields.decision, fields.now, fields.now).run();
  const byKey = await db.prepare('SELECT * FROM review_submissions WHERE idempotency_hash = ?').bind(fields.idempotencyHash).first();
  if (byKey && byKey.payload_hash !== fields.payloadHash) throw new HttpError(409, 'idempotency_key_reused');
  const byPayload = await db.prepare('SELECT * FROM review_submissions WHERE payload_hash = ?').bind(fields.payloadHash).first();
  if (!byPayload) throw new HttpError(503, 'submission_store_unavailable');
  return byPayload;
}

export async function onRequestPost({ request, env, params }) {
  let claimedRow = null;
  let leaseId = null;
  try {
    const { origin } = validateConfig(env);
    if (!exactOrigin(request, origin)) throw new HttpError(403, 'origin_rejected');
    const session = await getSession(request, env);
    if (!session) throw new HttpError(401, 'login_required');
    if (!await matchesCsrf(session.id, request.headers.get('X-LumaForge-CSRF'), env.SESSION_ENCRYPTION_KEY)) throw new HttpError(403, 'csrf_rejected');
    const key = idempotencyKey(request);
    if (!key) throw new HttpError(400, 'idempotency_key_required');
    const body = await readJson(request);
    const token = await accessTokenFor(session, env);
    await verifyAuthorizedUser(token);
    if (!await allowRate(env, `decision:${session.idHash}`, 8, 60)) throw new HttpError(429, 'rate_limited');
    const snapshot = await loadProductSnapshot();
    const reviewed = validateDecision(body, params?.featureId, snapshot, { enableDemo: env.ENABLE_REVIEW_DEMO === 'true' });
    const commentBody = serializeReviewComment(body);
    const now = Math.floor(Date.now() / 1000);
    const fields = {
      payloadHash: await sha256(commentBody),
      idempotencyHash: await sha256(key),
      featureId: body.feature,
      issue: reviewed.issue,
      revision: body.revision,
      decision: body.decision,
      now,
    };
    const existing = await reserve(env.REVIEW_DB, fields);
    if (existing.status === 'sent' || (existing.status === 'sending' && existing.lease_until > now)) return responseFor(existing);

    leaseId = crypto.randomUUID();
    const leaseUntil = now + 45;
    const claim = await env.REVIEW_DB.prepare(`
      UPDATE review_submissions SET status = 'sending', lease_id = ?, lease_until = ?, updated_at = ?
      WHERE payload_hash = ? AND (status IN ('reserved', 'retryable') OR (status = 'sending' AND lease_until <= ?))
    `).bind(leaseId, leaseUntil, now, fields.payloadHash, now).run();
    claimedRow = await env.REVIEW_DB.prepare('SELECT * FROM review_submissions WHERE payload_hash = ?').bind(fields.payloadHash).first();
    if (!claim.meta?.changes) return responseFor(claimedRow);

    const oldComment = await findExistingComment(reviewed.issue, commentBody, token, claimedRow.created_at * 1000);
    const comment = oldComment || await createIssueComment(reviewed.issue, commentBody, token);
    const url = canonicalIssueCommentUrl(reviewed.issue, comment.id);
    await env.REVIEW_DB.prepare(`
      UPDATE review_submissions SET status = 'sent', lease_id = NULL, lease_until = NULL, updated_at = ?, comment_id = ?, comment_url = ?
      WHERE payload_hash = ? AND lease_id = ?
    `).bind(Math.floor(Date.now() / 1000), comment.id, url, fields.payloadHash, leaseId).run();
    const sent = await env.REVIEW_DB.prepare('SELECT * FROM review_submissions WHERE payload_hash = ?').bind(fields.payloadHash).first();
    return responseFor(sent);
  } catch (error) {
    if (claimedRow && leaseId) {
      try {
        await env.REVIEW_DB.prepare(`UPDATE review_submissions SET status = 'retryable', lease_id = NULL, lease_until = NULL, updated_at = ?
          WHERE payload_hash = ? AND lease_id = ? AND status = 'sending'`)
          .bind(Math.floor(Date.now() / 1000), claimedRow.payload_hash, leaseId).run();
      } catch { /* The lease expiry permits a later idempotent retry. */ }
    }
    const status = error instanceof HttpError ? error.status : error instanceof GitHubError ? (error.status === 401 ? 401 : 503) : 503;
    const code = error instanceof HttpError ? error.code : error instanceof GitHubError && error.status === 401 ? 'session_expired' : 'github_unavailable';
    return jsonResponse(status, { error: code });
  }
}

export async function onRequestGet() {
  return jsonResponse(405, { error: 'method_not_allowed' }, { Allow: 'POST' });
}
