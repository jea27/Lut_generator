import { bytesToBase64Url, encryptSecret, HttpError, jsonResponse, masterKeyBytes, randomToken, redirectResponse, setCookie, sha256 } from '../../../_lib/security.mjs';
import { allowRate, OAUTH_COOKIE, validateConfig } from '../../../_lib/session.mjs';

export async function onRequestGet({ request, env }) {
  try {
    const { origin, callbackUrl } = validateConfig(env);
    masterKeyBytes(env.SESSION_ENCRYPTION_KEY);
    const ip = request.headers.get('CF-Connecting-IP');
    const rateIdentity = typeof ip === 'string' && ip.length <= 64 ? `oauth:${ip}` : 'oauth:unknown';
    if (!await allowRate(env, rateIdentity, 10, 60)) throw new HttpError(429, 'rate_limited');
    const state = randomToken();
    const verifier = randomToken(48);
    const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(verifier));
    const challengeBase64 = bytesToBase64Url(new Uint8Array(digest));
    const encryptedVerifier = await encryptSecret(verifier, env.SESSION_ENCRYPTION_KEY, 'oauth-pkce-verifier');
    const now = Math.floor(Date.now() / 1000);
    await env.REVIEW_DB.prepare('DELETE FROM oauth_states WHERE expires_at <= ? OR consumed_at IS NOT NULL').bind(now).run();
    await env.REVIEW_DB.prepare('INSERT INTO oauth_states (state_hash, verifier_ciphertext, created_at, expires_at) VALUES (?, ?, ?, ?)')
      .bind(await sha256(state), encryptedVerifier, now, now + 600).run();
    const auth = new URL('https://github.com/login/oauth/authorize');
    auth.search = new URLSearchParams({
      client_id: env.GITHUB_APP_CLIENT_ID,
      redirect_uri: callbackUrl,
      state,
      scope: 'offline_access',
      login: 'jea27',
      allow_signup: 'false',
      code_challenge: challengeBase64,
      code_challenge_method: 'S256',
    }).toString();
    return redirectResponse(auth.href, setCookie(OAUTH_COOKIE, state, 600));
  } catch (error) {
    const status = error instanceof HttpError ? error.status : 503;
    const code = error instanceof HttpError ? error.code : 'service_unavailable';
    return jsonResponse(status, { enabled: true, authenticated: false, error: code });
  }
}
