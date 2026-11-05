import { exchangeCode, revokeAppAuthorization, verifyAuthorizedUser } from '../../../_lib/github.mjs';
import { cookieValue, decryptSecret, HttpError, masterKeyBytes, redirectResponse, setCookie, sha256 } from '../../../_lib/security.mjs';
import { createSession, OAUTH_COOKIE, SESSION_COOKIE, SESSION_IDLE_SECONDS, validateConfig } from '../../../_lib/session.mjs';

function returnTo(origin, ok, sessionId = null) {
  const headers = new Headers({
    'Cache-Control': 'no-store, max-age=0',
    'Location': `${origin}/?auth=${ok ? 'complete' : 'failed'}#reviews`,
    'Referrer-Policy': 'no-referrer',
    'X-Content-Type-Options': 'nosniff',
  });
  headers.append('Set-Cookie', setCookie(OAUTH_COOKIE, '', 0));
  if (sessionId) headers.append('Set-Cookie', setCookie(SESSION_COOKIE, sessionId, SESSION_IDLE_SECONDS));
  return new Response(null, { status: 303, headers });
}

export async function onRequestGet({ request, env }) {
  let tokens = null;
  let sessionCreated = false;
  try {
    const { origin, callbackUrl } = validateConfig(env);
    masterKeyBytes(env.SESSION_ENCRYPTION_KEY);
    const url = new URL(request.url);
    const state = url.searchParams.get('state');
    const code = url.searchParams.get('code');
    const cookie = cookieValue(request, OAUTH_COOKIE);
    if (!state || !cookie || state !== cookie || !/^[A-Za-z0-9_-]{40,128}$/.test(state) ||
        !code || code.length > 512 || !/^[A-Za-z0-9_-]+$/.test(code) || url.searchParams.has('error')) {
      return returnTo(origin, false);
    }
    const now = Math.floor(Date.now() / 1000);
    const stateHash = await sha256(state);
    const claimed = await env.REVIEW_DB.prepare(`
      UPDATE oauth_states SET consumed_at = ?
      WHERE state_hash = ? AND consumed_at IS NULL AND expires_at > ?
      RETURNING verifier_ciphertext
    `).bind(now, stateHash, now).first();
    if (!claimed?.verifier_ciphertext) return returnTo(origin, false);
    const verifier = await decryptSecret(claimed.verifier_ciphertext, env.SESSION_ENCRYPTION_KEY, 'oauth-pkce-verifier');
    tokens = await exchangeCode(env, code, verifier, callbackUrl);
    await verifyAuthorizedUser(tokens.accessToken);
    const sessionId = await createSession(env, tokens, now);
    sessionCreated = true;
    tokens = null;
    return returnTo(origin, true, sessionId);
  } catch (error) {
    if (tokens && !sessionCreated) await revokeAppAuthorization(env, tokens.accessToken);
    let origin = null;
    try { origin = validateConfig(env).origin; } catch { /* Return a generic server response below. */ }
    if (origin) return returnTo(origin, false);
    const status = error instanceof HttpError ? error.status : 503;
    return new Response(JSON.stringify({ enabled: true, authenticated: false, error: 'service_unavailable' }), {
      status,
      headers: {
        'Cache-Control': 'no-store, max-age=0',
        'Content-Type': 'application/json; charset=utf-8',
        'Referrer-Policy': 'no-referrer',
        'X-Content-Type-Options': 'nosniff',
      },
    });
  }
}
