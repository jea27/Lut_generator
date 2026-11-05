export const GITHUB_OWNER = 'jea27';
export const GITHUB_REPO = 'Lut_generator';
export const GITHUB_REPOSITORY_ID = '1439840068';
export const AUTHORIZED_LOGIN = 'jea27';
export const AUTHORIZED_USER_ID = 45896918;
export const GITHUB_API_VERSION = '2022-11-28';
const API = 'https://api.github.com';

export class GitHubError extends Error {
  constructor(status = 503, code = 'github_unavailable') {
    super(code);
    this.status = status;
    this.code = code;
  }
}

async function timedFetch(url, init, timeoutMs = 12000) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    return await fetch(url, { ...init, redirect: 'error', signal: controller.signal });
  } catch {
    throw new GitHubError(503, 'github_unavailable');
  } finally {
    clearTimeout(timer);
  }
}

export async function githubJson(path, token, init = {}) {
  if (typeof path !== 'string' || !path.startsWith('/') || path.startsWith('//') || path.includes('..')) throw new Error('invalid_github_path');
  const response = await timedFetch(`${API}${path}`, {
    ...init,
    headers: {
      Accept: 'application/vnd.github+json',
      Authorization: `Bearer ${token}`,
      'X-GitHub-Api-Version': GITHUB_API_VERSION,
      'User-Agent': 'LumaForge-Project-OS',
      ...(init.headers || {}),
    },
  });
  if (!response.ok) throw new GitHubError(response.status, response.status === 401 ? 'github_unauthorized' : 'github_unavailable');
  const length = Number(response.headers.get('Content-Length'));
  if (Number.isFinite(length) && length > 2 * 1024 * 1024) throw new GitHubError(503, 'github_unavailable');
  try {
    const raw = await response.text();
    if (new TextEncoder().encode(raw).byteLength > 2 * 1024 * 1024) throw new Error('response_too_large');
    return JSON.parse(raw);
  } catch {
    throw new GitHubError(503, 'github_unavailable');
  }
}

export async function exchangeCode(env, code, verifier, redirectUri) {
  const form = new URLSearchParams({
    client_id: env.GITHUB_APP_CLIENT_ID,
    client_secret: env.GITHUB_APP_CLIENT_SECRET,
    code,
    redirect_uri: redirectUri,
    code_verifier: verifier,
    repository_id: GITHUB_REPOSITORY_ID,
  });
  const response = await timedFetch('https://github.com/login/oauth/access_token', {
    method: 'POST',
    headers: { Accept: 'application/json', 'Content-Type': 'application/x-www-form-urlencoded' },
    body: form,
  });
  if (!response.ok) throw new GitHubError(503, 'github_unavailable');
  let data;
  try { data = await response.json(); } catch { throw new GitHubError(503, 'github_unavailable'); }
  if (typeof data.access_token !== 'string' || data.access_token.length < 20 || data.access_token.length > 512 ||
      typeof data.refresh_token !== 'string' || data.refresh_token.length < 20 || data.refresh_token.length > 512 ||
      data.token_type !== 'bearer' || !Number.isInteger(data.expires_in) || data.expires_in < 60 || data.expires_in > 28800 ||
      !Number.isInteger(data.refresh_token_expires_in) || data.refresh_token_expires_in < 60 || data.refresh_token_expires_in > 15897600) {
    throw new GitHubError(503, 'github_unavailable');
  }
  return {
    accessToken: data.access_token,
    refreshToken: data.refresh_token,
    accessExpiresIn: data.expires_in,
    refreshExpiresIn: data.refresh_token_expires_in,
  };
}

export async function refreshUserToken(env, refreshToken) {
  const form = new URLSearchParams({
    client_id: env.GITHUB_APP_CLIENT_ID,
    client_secret: env.GITHUB_APP_CLIENT_SECRET,
    grant_type: 'refresh_token',
    refresh_token: refreshToken,
  });
  const response = await timedFetch('https://github.com/login/oauth/access_token', {
    method: 'POST',
    headers: { Accept: 'application/json', 'Content-Type': 'application/x-www-form-urlencoded' },
    body: form,
  });
  if (!response.ok) throw new GitHubError(503, 'github_unavailable');
  let data;
  try { data = await response.json(); } catch { throw new GitHubError(503, 'github_unavailable'); }
  if (typeof data.access_token !== 'string' || data.access_token.length < 20 || data.access_token.length > 512 ||
      typeof data.refresh_token !== 'string' || data.refresh_token.length < 20 || data.refresh_token.length > 512 ||
      data.token_type !== 'bearer' || !Number.isInteger(data.expires_in) || data.expires_in < 60 || data.expires_in > 28800 ||
      !Number.isInteger(data.refresh_token_expires_in) || data.refresh_token_expires_in < 60 || data.refresh_token_expires_in > 15897600) {
    throw new GitHubError(401, 'github_unauthorized');
  }
  return {
    accessToken: data.access_token,
    refreshToken: data.refresh_token,
    accessExpiresIn: data.expires_in,
    refreshExpiresIn: data.refresh_token_expires_in,
  };
}

export async function verifyAuthorizedUser(token) {
  const user = await githubJson('/user', token);
  if (user?.type !== 'User' || user?.login !== AUTHORIZED_LOGIN || user?.id !== AUTHORIZED_USER_ID) {
    throw new GitHubError(403, 'github_user_not_authorized');
  }
  // Issue 77 is a harmless read proving that the authorization and installation
  // can reach the one repository configured for this review app.
  await githubJson(`/repos/${GITHUB_OWNER}/${GITHUB_REPO}/issues/77`, token);
  return { login: user.login, id: user.id, type: user.type };
}

function base64(value) {
  let binary = '';
  for (const byte of new TextEncoder().encode(value)) binary += String.fromCharCode(byte);
  return btoa(binary);
}

export async function revokeAppAuthorization(env, accessToken) {
  if (!accessToken) return;
  try {
    await timedFetch(`https://api.github.com/applications/${encodeURIComponent(env.GITHUB_APP_CLIENT_ID)}/grant`, {
      method: 'DELETE',
      headers: {
        Accept: 'application/vnd.github+json',
        Authorization: `Basic ${base64(`${env.GITHUB_APP_CLIENT_ID}:${env.GITHUB_APP_CLIENT_SECRET}`)}`,
        'Content-Type': 'application/json',
        'X-GitHub-Api-Version': GITHUB_API_VERSION,
        'User-Agent': 'LumaForge-Project-OS',
      },
      body: JSON.stringify({ access_token: accessToken }),
    });
  } catch {
    // Local session revocation is authoritative even if remote revocation is down.
  }
}

export async function findExistingComment(issue, body, token, createdAt) {
  const since = new Date(Math.max(0, createdAt - 60_000)).toISOString();
  for (let page = 1; page <= 10; page += 1) {
    const query = new URLSearchParams({ since, per_page: '100', sort: 'created', direction: 'desc', page: String(page) });
    const comments = await githubJson(`/repos/${GITHUB_OWNER}/${GITHUB_REPO}/issues/${issue}/comments?${query}`, token);
    if (!Array.isArray(comments)) throw new GitHubError(503, 'github_unavailable');
    const match = comments.find(comment => comment?.body === body && comment?.user?.type === 'User' &&
      comment.user.login === AUTHORIZED_LOGIN && comment.user.id === AUTHORIZED_USER_ID && Number.isSafeInteger(comment.id) &&
      Date.parse(comment.created_at || '') >= createdAt - 60_000);
    if (match) return match;
    if (comments.length < 100) break;
    const oldest = Date.parse(comments.at(-1)?.created_at || '');
    if (Number.isFinite(oldest) && oldest < createdAt - 60_000) break;
  }
  return null;
}

export async function createIssueComment(issue, body, token) {
  const comment = await githubJson(`/repos/${GITHUB_OWNER}/${GITHUB_REPO}/issues/${issue}/comments`, token, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ body }),
  });
  if (!Number.isSafeInteger(comment?.id) || comment.id < 1 || comment?.user?.login !== AUTHORIZED_LOGIN || comment?.user?.id !== AUTHORIZED_USER_ID) {
    throw new GitHubError(503, 'github_unavailable');
  }
  return comment;
}
