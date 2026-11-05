import { decryptSecret, encryptSecret, hmac, HttpError, randomToken, sha256 } from './security.mjs';
import { GitHubError, refreshUserToken, revokeAppAuthorization, verifyAuthorizedUser } from './github.mjs';

export const SESSION_COOKIE = '__Host-lf_session';
export const OAUTH_COOKIE = '__Host-lf_oauth';
export const SESSION_IDLE_SECONDS = 7 * 24 * 60 * 60;
const ACCESS_REFRESH_SKEW_SECONDS = 120;

export function validateConfig(env) {
  const origin = env.ALLOWED_ORIGIN;
  let parsed;
  try { parsed = new URL(origin); } catch { parsed = null; }
  if (!env.REVIEW_DB || !env.GITHUB_APP_CLIENT_ID || !env.GITHUB_APP_CLIENT_SECRET || !env.SESSION_ENCRYPTION_KEY ||
      !parsed || parsed.protocol !== 'https:' || parsed.origin !== origin || parsed.pathname !== '/' || parsed.search || parsed.hash) {
    throw new HttpError(503, 'service_not_configured');
  }
  return { origin, callbackUrl: `${origin}/api/auth/github/callback` };
}

export async function allowRate(env, identifier, limit, windowSeconds = 60, now = Math.floor(Date.now() / 1000)) {
  const bucket = Math.floor(now / windowSeconds);
  if (bucket % 60 === 0) {
    await env.REVIEW_DB.prepare('DELETE FROM rate_limits WHERE expires_at <= ?').bind(now).run();
  }
  const keyHash = await hmac(`rate-v1:${identifier}`, env.SESSION_ENCRYPTION_KEY);
  const result = await env.REVIEW_DB.prepare(`
    INSERT INTO rate_limits (key_hash, bucket, hit_count, expires_at)
    VALUES (?, ?, 1, ?)
    ON CONFLICT (key_hash, bucket) DO UPDATE SET hit_count = hit_count + 1
      WHERE hit_count < ?
    RETURNING hit_count
  `).bind(keyHash, bucket, (bucket + 2) * windowSeconds, limit).first();
  return Boolean(result);
}

export async function getSession(request, env, now = Math.floor(Date.now() / 1000)) {
  const rawId = (request.headers.get('Cookie') || '').split(';').map(part => part.trim()).filter(part => part.startsWith(`${SESSION_COOKIE}=`));
  if (rawId.length !== 1) return null;
  const sessionId = rawId[0].slice(SESSION_COOKIE.length + 1);
  if (!/^[A-Za-z0-9_-]{40,128}$/.test(sessionId)) return null;
  const idHash = await sha256(sessionId);
  const row = await env.REVIEW_DB.prepare(`
    SELECT * FROM review_sessions WHERE id_hash = ? AND revoked_at IS NULL AND expires_at > ?
  `).bind(idHash, now).first();
  if (!row || row.github_login !== 'jea27' || row.github_user_id !== 45896918 || !row.access_token_ciphertext || !row.refresh_token_ciphertext) return null;
  return { id: sessionId, idHash, row };
}

async function storeRefreshed(session, env, leaseId, tokens, now) {
  const accessCiphertext = await encryptSecret(tokens.accessToken, env.SESSION_ENCRYPTION_KEY, 'github-access-token');
  const refreshCiphertext = await encryptSecret(tokens.refreshToken, env.SESSION_ENCRYPTION_KEY, 'github-refresh-token');
  const result = await env.REVIEW_DB.prepare(`
    UPDATE review_sessions
    SET access_token_ciphertext = ?, refresh_token_ciphertext = ?, access_expires_at = ?, refresh_expires_at = ?,
        refresh_lease_id = NULL, refresh_lease_until = NULL, last_seen_at = ?, expires_at = ?
    WHERE id_hash = ? AND refresh_lease_id = ? AND revoked_at IS NULL
  `).bind(accessCiphertext, refreshCiphertext, now + tokens.accessExpiresIn, now + tokens.refreshExpiresIn,
    now, now + SESSION_IDLE_SECONDS, session.idHash, leaseId).run();
  if (!result.meta?.changes) throw new HttpError(401, 'session_expired');
  return tokens.accessToken;
}

export async function accessTokenFor(session, env, now = Math.floor(Date.now() / 1000)) {
  let row = session.row;
  if (row.access_expires_at > now + ACCESS_REFRESH_SKEW_SECONDS) {
    return decryptSecret(row.access_token_ciphertext, env.SESSION_ENCRYPTION_KEY, 'github-access-token');
  }
  if (!row.refresh_token_ciphertext || row.refresh_expires_at <= now) {
    await revokeSession(session, env, now);
    throw new HttpError(401, 'session_expired');
  }

  const leaseId = randomToken();
  const leaseUntil = now + 30;
  const claimed = await env.REVIEW_DB.prepare(`
    UPDATE review_sessions SET refresh_lease_id = ?, refresh_lease_until = ?
    WHERE id_hash = ? AND revoked_at IS NULL AND refresh_expires_at > ?
      AND (refresh_lease_until IS NULL OR refresh_lease_until < ?)
  `).bind(leaseId, leaseUntil, session.idHash, now, now).run();
  if (!claimed.meta?.changes) {
    for (let attempt = 0; attempt < 12; attempt += 1) {
      await new Promise(resolve => setTimeout(resolve, 150));
      row = await env.REVIEW_DB.prepare('SELECT * FROM review_sessions WHERE id_hash = ? AND revoked_at IS NULL AND expires_at > ?')
        .bind(session.idHash, now).first();
      if (!row || !row.access_token_ciphertext) break;
      if (row.access_expires_at > now + ACCESS_REFRESH_SKEW_SECONDS) {
        session.row = row;
        return decryptSecret(row.access_token_ciphertext, env.SESSION_ENCRYPTION_KEY, 'github-access-token');
      }
    }
    throw new HttpError(503, 'session_refresh_pending');
  }

  try {
    const refreshToken = await decryptSecret(row.refresh_token_ciphertext, env.SESSION_ENCRYPTION_KEY, 'github-refresh-token');
    const tokens = await refreshUserToken(env, refreshToken);
    await verifyAuthorizedUser(tokens.accessToken);
    const accessToken = await storeRefreshed(session, env, leaseId, tokens, now);
    session.row = { ...row, access_expires_at: now + tokens.accessExpiresIn };
    return accessToken;
  } catch (error) {
    await env.REVIEW_DB.prepare(`UPDATE review_sessions SET refresh_lease_id = NULL, refresh_lease_until = NULL
      WHERE id_hash = ? AND refresh_lease_id = ?`).bind(session.idHash, leaseId).run();
    if (error instanceof GitHubError && (error.status === 401 || error.status === 403)) {
      await revokeSession(session, env, now);
      throw new HttpError(401, 'session_expired');
    }
    if (error instanceof HttpError) throw error;
    throw new HttpError(503, 'github_unavailable');
  }
}

export async function createSession(env, tokens, now = Math.floor(Date.now() / 1000)) {
  const id = randomToken();
  const idHash = await sha256(id);
  const accessCiphertext = await encryptSecret(tokens.accessToken, env.SESSION_ENCRYPTION_KEY, 'github-access-token');
  const refreshCiphertext = await encryptSecret(tokens.refreshToken, env.SESSION_ENCRYPTION_KEY, 'github-refresh-token');
  await env.REVIEW_DB.prepare(`
    INSERT INTO review_sessions (id_hash, github_user_id, github_login, access_token_ciphertext, refresh_token_ciphertext,
      access_expires_at, refresh_expires_at, created_at, last_seen_at, expires_at)
    VALUES (?, 45896918, 'jea27', ?, ?, ?, ?, ?, ?, ?)
  `).bind(idHash, accessCiphertext, refreshCiphertext, now + tokens.accessExpiresIn,
    now + tokens.refreshExpiresIn, now, now, now + SESSION_IDLE_SECONDS).run();
  return id;
}

export async function revokeSession(session, env, now = Math.floor(Date.now() / 1000)) {
  let token = null;
  try {
    if (session.row.access_token_ciphertext) token = await decryptSecret(session.row.access_token_ciphertext, env.SESSION_ENCRYPTION_KEY, 'github-access-token');
  } catch { /* Erase the unusable local ciphertext below. */ }
  await env.REVIEW_DB.prepare(`UPDATE review_sessions SET revoked_at = ?, access_token_ciphertext = NULL,
    refresh_token_ciphertext = NULL, refresh_lease_id = NULL, refresh_lease_until = NULL
    WHERE id_hash = ? AND revoked_at IS NULL`).bind(now, session.idHash).run();
  await revokeAppAuthorization(env, token);
}

export async function authorizeSession(request, env) {
  let session;
  try { session = await getSession(request, env); }
  catch { throw new HttpError(503, 'session_store_unavailable'); }
  if (!session) throw new HttpError(401, 'login_required');
  return { session, token: await accessTokenFor(session, env) };
}
