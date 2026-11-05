import { verifyAuthorizedUser } from '../../_lib/github.mjs';
import { csrfToken, cookieValue, HttpError, jsonResponse, matchesCsrf, setCookie } from '../../_lib/security.mjs';
import { accessTokenFor, getSession, SESSION_COOKIE, SESSION_IDLE_SECONDS, validateConfig } from '../../_lib/session.mjs';

export async function onRequestGet({ request, env }) {
  try {
    validateConfig(env);
    const session = await getSession(request, env);
    if (!session) return jsonResponse(200, { enabled: true, authenticated: false });
    const token = await accessTokenFor(session, env);
    await verifyAuthorizedUser(token);
    const now = Math.floor(Date.now() / 1000);
    await env.REVIEW_DB.prepare('UPDATE review_sessions SET last_seen_at = ?, expires_at = ? WHERE id_hash = ? AND revoked_at IS NULL')
      .bind(now, now + SESSION_IDLE_SECONDS, session.idHash).run();
    return jsonResponse(200, { enabled: true, authenticated: true, login: 'jea27', csrf: await csrfToken(session.id, env.SESSION_ENCRYPTION_KEY) }, {
      'Set-Cookie': setCookie(SESSION_COOKIE, session.id, SESSION_IDLE_SECONDS),
    });
  } catch (error) {
    const status = error instanceof HttpError ? error.status : 503;
    const code = error instanceof HttpError ? error.code : 'service_unavailable';
    return jsonResponse(status, { enabled: true, authenticated: false, error: code });
  }
}

export async function onRequestPost({ request, env }) {
  return jsonResponse(405, { error: 'method_not_allowed' }, { Allow: 'GET' });
}
