import { exactOrigin, cookieValue, HttpError, jsonResponse, matchesCsrf, setCookie } from '../../_lib/security.mjs';
import { getSession, revokeSession, SESSION_COOKIE, validateConfig } from '../../_lib/session.mjs';

export async function onRequestPost({ request, env }) {
  try {
    const { origin } = validateConfig(env);
    if (!exactOrigin(request, origin)) throw new HttpError(403, 'origin_rejected');
    const session = await getSession(request, env);
    if (!session) return jsonResponse(200, { enabled: true, authenticated: false }, { 'Set-Cookie': setCookie(SESSION_COOKIE, '', 0) });
    if (!await matchesCsrf(session.id, request.headers.get('X-LumaForge-CSRF'), env.SESSION_ENCRYPTION_KEY)) throw new HttpError(403, 'csrf_rejected');
    await revokeSession(session, env);
    return jsonResponse(200, { enabled: true, authenticated: false }, { 'Set-Cookie': setCookie(SESSION_COOKIE, '', 0) });
  } catch (error) {
    const status = error instanceof HttpError ? error.status : 503;
    const code = error instanceof HttpError ? error.code : 'service_unavailable';
    return jsonResponse(status, { error: code });
  }
}

export async function onRequestGet() {
  return jsonResponse(405, { error: 'method_not_allowed' }, { Allow: 'POST' });
}
