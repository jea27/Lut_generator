const encoder = new TextEncoder();
const KEY_SALT = encoder.encode('lumaforge-project-os/auth-v1');

export function bytesToBase64Url(bytes) {
  let binary = '';
  for (const byte of bytes) binary += String.fromCharCode(byte);
  return btoa(binary).replace(/=/g, '').replace(/\+/g, '-').replace(/\//g, '_');
}

export function base64ToBytes(value) {
  if (typeof value !== 'string' || !/^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/.test(value)) {
    throw new Error('invalid_key');
  }
  const binary = atob(value);
  return Uint8Array.from(binary, character => character.charCodeAt(0));
}

export function base64UrlToBytes(value) {
  if (typeof value !== 'string' || !/^[A-Za-z0-9_-]+$/.test(value)) throw new Error('invalid_encoding');
  const base64 = value.replace(/-/g, '+').replace(/_/g, '/');
  return base64ToBytes(base64 + '='.repeat((4 - base64.length % 4) % 4));
}

export function masterKeyBytes(value) {
  const bytes = base64ToBytes(value);
  if (bytes.byteLength !== 32) throw new Error('invalid_key');
  return bytes;
}

export function randomBytes(length = 32) {
  const bytes = new Uint8Array(length);
  crypto.getRandomValues(bytes);
  return bytes;
}

export function randomToken(length = 32) {
  return bytesToBase64Url(randomBytes(length));
}

export async function sha256(value) {
  const input = typeof value === 'string' ? encoder.encode(value) : value;
  const digest = await crypto.subtle.digest('SHA-256', input);
  return [...new Uint8Array(digest)].map(byte => byte.toString(16).padStart(2, '0')).join('');
}

export async function hmac(value, secret) {
  const keyBytes = typeof secret === 'string' ? masterKeyBytes(secret) : secret;
  const key = await crypto.subtle.importKey('raw', keyBytes, { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const signature = await crypto.subtle.sign('HMAC', key, encoder.encode(value));
  return bytesToBase64Url(new Uint8Array(signature));
}

function constantTimeEqual(left, right) {
  if (typeof left !== 'string' || typeof right !== 'string') return false;
  let mismatch = left.length ^ right.length;
  const length = Math.max(left.length, right.length);
  for (let index = 0; index < length; index += 1) {
    mismatch |= (left.charCodeAt(index) || 0) ^ (right.charCodeAt(index) || 0);
  }
  return mismatch === 0;
}

export async function verifyHmac(value, signature, secret) {
  return constantTimeEqual(await hmac(value, secret), signature);
}

async function deriveAesKey(secret) {
  const material = await crypto.subtle.importKey('raw', masterKeyBytes(secret), 'HKDF', false, ['deriveKey']);
  return crypto.subtle.deriveKey(
    { name: 'HKDF', hash: 'SHA-256', salt: KEY_SALT, info: encoder.encode('token-encryption') },
    material,
    { name: 'AES-GCM', length: 256 },
    false,
    ['encrypt', 'decrypt'],
  );
}

export async function encryptSecret(plaintext, secret, purpose) {
  if (typeof plaintext !== 'string' || plaintext.length === 0) throw new Error('invalid_secret');
  const iv = randomBytes(12);
  const key = await deriveAesKey(secret);
  const encrypted = await crypto.subtle.encrypt(
    { name: 'AES-GCM', iv, additionalData: encoder.encode(`lumaforge:${purpose}:v1`) },
    key,
    encoder.encode(plaintext),
  );
  return `${bytesToBase64Url(iv)}.${bytesToBase64Url(new Uint8Array(encrypted))}`;
}

export async function decryptSecret(ciphertext, secret, purpose) {
  if (typeof ciphertext !== 'string') throw new Error('invalid_ciphertext');
  const parts = ciphertext.split('.');
  if (parts.length !== 2) throw new Error('invalid_ciphertext');
  const iv = base64UrlToBytes(parts[0]);
  const encrypted = base64UrlToBytes(parts[1]);
  if (iv.byteLength !== 12 || encrypted.byteLength < 17) throw new Error('invalid_ciphertext');
  const key = await deriveAesKey(secret);
  const plaintext = await crypto.subtle.decrypt(
    { name: 'AES-GCM', iv, additionalData: encoder.encode(`lumaforge:${purpose}:v1`) },
    key,
    encrypted,
  );
  return new TextDecoder().decode(plaintext);
}

export function cookieValue(request, name) {
  const header = request.headers.get('Cookie') || '';
  const matches = header.split(';').map(part => part.trim()).filter(part => part.startsWith(`${name}=`));
  if (matches.length !== 1) return null;
  const value = matches[0].slice(name.length + 1);
  return /^[A-Za-z0-9_-]{40,128}$/.test(value) ? value : null;
}

export function setCookie(name, value, maxAge) {
  const safeName = /^[A-Za-z0-9_-]+$/.test(name);
  const safeValue = value === '' || /^[A-Za-z0-9_-]{40,128}$/.test(value);
  if (!safeName || !safeValue || !Number.isInteger(maxAge) || maxAge < 0) throw new Error('invalid_cookie');
  return `${name}=${value}; Max-Age=${maxAge}; Path=/; Secure; HttpOnly; SameSite=Lax`;
}

export async function csrfToken(sessionId, secret) {
  return hmac(`csrf-v1:${sessionId}`, secret);
}

export async function matchesCsrf(sessionId, token, secret) {
  if (typeof token !== 'string' || !/^[A-Za-z0-9_-]{40,64}$/.test(token)) return false;
  return verifyHmac(`csrf-v1:${sessionId}`, token, secret);
}

export function exactOrigin(request, allowedOrigin) {
  const origin = request.headers.get('Origin');
  return Boolean(origin && origin === allowedOrigin && request.headers.get('Sec-Fetch-Site') !== 'cross-site');
}

export function parseAllowedOrigin(value) {
  try {
    const parsed = new URL(value);
    if (parsed.protocol !== 'https:' || parsed.origin !== value || parsed.pathname !== '/' || parsed.search || parsed.hash || parsed.username || parsed.password) return null;
    return parsed.origin;
  } catch {
    return null;
  }
}

export function responseHeaders(extra = {}) {
  return new Headers({
    'Cache-Control': 'no-store, max-age=0',
    'Content-Type': 'application/json; charset=utf-8',
    'Pragma': 'no-cache',
    'Referrer-Policy': 'no-referrer',
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    ...extra,
  });
}

export function jsonResponse(status, body, extraHeaders = {}) {
  return new Response(JSON.stringify(body), { status, headers: responseHeaders(extraHeaders) });
}

export function redirectResponse(url, cookie = null) {
  const headers = new Headers({
    'Cache-Control': 'no-store, max-age=0',
    'Location': url,
    'Referrer-Policy': 'no-referrer',
    'X-Content-Type-Options': 'nosniff',
  });
  if (cookie) headers.append('Set-Cookie', cookie);
  return new Response(null, { status: 303, headers });
}

export class HttpError extends Error {
  constructor(status, code) {
    super(code);
    this.status = status;
    this.code = code;
  }
}

export async function readJson(request, maxBytes = 8192) {
  const type = request.headers.get('Content-Type')?.split(';', 1)[0].trim().toLowerCase();
  if (type !== 'application/json') throw new HttpError(415, 'json_required');
  const declared = Number(request.headers.get('Content-Length'));
  if (Number.isFinite(declared) && declared > maxBytes) throw new HttpError(413, 'request_too_large');
  const text = await request.text();
  if (new TextEncoder().encode(text).byteLength > maxBytes) throw new HttpError(413, 'request_too_large');
  try {
    return JSON.parse(text);
  } catch {
    throw new HttpError(400, 'invalid_json');
  }
}
