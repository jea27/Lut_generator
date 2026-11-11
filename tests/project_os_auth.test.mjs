import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { DatabaseSync } from 'node:sqlite';
import test, { afterEach } from 'node:test';
import { onRequestPost as submitDecision } from '../functions/api/reviews/[featureId]/decision.js';
import { onRequestGet as startLogin } from '../functions/api/auth/github/start.js';
import { verifyAuthorizedUser } from '../functions/_lib/github.mjs';
import { validateDecision, serializeReviewComment } from '../functions/_lib/product.mjs';
import { csrfToken, decryptSecret, encryptSecret, exactOrigin, matchesCsrf, masterKeyBytes, setCookie } from '../functions/_lib/security.mjs';
import { createSession, SESSION_COOKIE } from '../functions/_lib/session.mjs';

const secret = btoa(String.fromCharCode(...new Uint8Array(32).fill(7)));
const originalFetch = globalThis.fetch;

function sqliteD1() {
  const sqlite = new DatabaseSync(':memory:');
  const migration = awaitable(readFile(new URL('../migrations/0001_project_os_auth.sql', import.meta.url), 'utf8'));
  return migration.then(sql => {
    sqlite.exec(sql);
    return {
      prepare(query) {
        return { bind(...values) {
          return {
            first() { return sqlite.prepare(query).get(...values) || null; },
            run() { const result = sqlite.prepare(query).run(...values); return { meta: { changes: Number(result.changes) } }; },
            all() { return { results: sqlite.prepare(query).all(...values) }; },
          };
        } };
      },
      close() { sqlite.close(); },
    };
  });
}

function awaitable(value) { return value; }

function testSnapshot() {
  const snapshot = structuredClone(JSON.parse(requirelessProductJson));
  snapshot.reviews_active = true;
  snapshot.sync.observed_at = new Date().toISOString();
  return snapshot;
}

let requirelessProductJson;
const productJsonPromise = readFile(new URL('../site/data/product.json', import.meta.url), 'utf8').then(value => { requirelessProductJson = value; });
const activeDbs = new Set();
afterEach(() => {
  globalThis.fetch = originalFetch;
  for (const db of activeDbs) db.close();
  activeDbs.clear();
});

test('secret encryption, purpose binding, CSRF and secure cookie attributes', async () => {
  masterKeyBytes(secret);
  const token = 'ghu_example-token-that-is-never-returned-to-the-browser';
  const ciphertext = await encryptSecret(token, secret, 'github-access-token');
  assert.notEqual(ciphertext, token);
  assert.equal(await decryptSecret(ciphertext, secret, 'github-access-token'), token);
  await assert.rejects(decryptSecret(ciphertext, secret, 'github-refresh-token'));
  const csrf = await csrfToken('opaque-session-id-123456789012345678901234567890123456', secret);
  assert.equal(await matchesCsrf('opaque-session-id-123456789012345678901234567890123456', csrf, secret), true);
  assert.equal(await matchesCsrf('other-session-id-1234567890123456789012345678901234567', csrf, secret), false);
  assert.match(setCookie('__Host-lf_session', 'a'.repeat(43), 600), /Secure; HttpOnly; SameSite=Lax$/);
  assert.equal(exactOrigin(new Request('https://project.test/api', { headers: { Origin: 'https://project.test' } }), 'https://project.test'), true);
  assert.equal(exactOrigin(new Request('https://project.test/api', { headers: { Origin: 'https://evil.test' } }), 'https://project.test'), false);
});

test('decision validation binds capability, checklist, issue and version', async () => {
  await productJsonPromise;
  const snapshot = testSnapshot();
  const feature = snapshot.features.find(item => item.id === 'manual-look');
  const valid = {
    feature: feature.id,
    revision: feature.review.context.revision,
    commit: feature.review.context.commit,
    version: feature.review.context.version,
    decision: 'approve',
    checklist: feature.checklist.map(item => item.id),
    notes: '',
  };
  assert.equal(validateDecision(valid, feature.id, snapshot).issue, 68);
  assert.throws(() => validateDecision({ ...valid, commit: '0'.repeat(40) }, feature.id, snapshot), { code: 'review_version_changed' });
  assert.throws(() => validateDecision({ ...valid, checklist: [] }, feature.id, snapshot), { code: 'checklist_incomplete' });
  assert.throws(() => validateDecision({ ...valid, feature: 'glow' }, feature.id, snapshot), { code: 'invalid_feature' });
  assert.throws(() => validateDecision({ ...valid, extra: 'ignored?' }, feature.id, snapshot), { code: 'invalid_decision' });
  const alteredIssue = structuredClone(snapshot);
  const alteredFeature = alteredIssue.features.find(item => item.id === 'manual-look');
  alteredFeature.issue_url = 'https://github.com/jea27/Lut_generator/issues/85';
  assert.throws(() => validateDecision(valid, feature.id, alteredIssue), { code: 'review_context_unavailable' });
  assert.throws(() => validateDecision({ ...valid, feature: 'review-demo', revision: snapshot.review_demo.review.context.revision,
    commit: snapshot.review_demo.review.context.commit, version: snapshot.review_demo.review.context.version,
    checklist: snapshot.review_demo.checklist.map(item => item.id) }, 'review-demo', snapshot), { code: 'demo_disabled' });
});

test('structured comment remains compatible with the existing issue_comment processor', () => {
  const payload = { feature: 'glow', revision: 'a'.repeat(64), commit: 'b'.repeat(40), version: '0.3.0', decision: 'changes', checklist: [], notes: 'Ajustar halos.' };
  assert.equal(serializeReviewComment(payload), `LUMAFORGE_REVIEW_V1\n\`\`\`json\n${JSON.stringify(payload, null, 2)}\n\`\`\``);
});

test('decision route checks CSRF/version and posts one attributed comment idempotently', async () => {
  await productJsonPromise;
  const db = await sqliteD1();
  activeDbs.add(db);
  const env = {
    REVIEW_DB: db,
    SESSION_ENCRYPTION_KEY: secret,
    GITHUB_APP_CLIENT_ID: 'Iv1.test-client-id',
    GITHUB_APP_CLIENT_SECRET: 'server-only-test-secret',
    ALLOWED_ORIGIN: 'https://project.test',
    ENABLE_REVIEW_DEMO: 'false',
  };
  const sessionId = await createSession(env, { accessToken: 'ghu_example-test-access-token-123456789', refreshToken: 'ghr_example-test-refresh-token-123456789', accessExpiresIn: 3600, refreshExpiresIn: 100000 });
  const csrf = await csrfToken(sessionId, secret);
  const snapshot = testSnapshot();
  const feature = snapshot.features.find(item => item.id === 'manual-look');
  const body = { feature: feature.id, revision: feature.review.context.revision, commit: feature.review.context.commit,
    version: feature.review.context.version, decision: 'approve', checklist: feature.checklist.map(item => item.id), notes: '' };
  let posts = 0;
  globalThis.fetch = async (input, init = {}) => {
    const url = String(input);
    if (url.startsWith('https://jea27.github.io/Lut_generator/data/product.json')) {
      return new Response(JSON.stringify(snapshot), { status: 200, headers: { 'Content-Type': 'application/json' } });
    }
    if (url === 'https://api.github.com/user') {
      assert.match(init.headers.Authorization, /^Bearer ghu_/);
      return Response.json({ id: 45896918, login: 'jea27', type: 'User' });
    }
    if (url === 'https://api.github.com/repos/jea27/Lut_generator/issues/77') return Response.json({ number: 77 });
    if (url.startsWith('https://api.github.com/repos/jea27/Lut_generator/issues/68/comments?')) return Response.json([]);
    if (url === 'https://api.github.com/repos/jea27/Lut_generator/issues/68/comments' && init.method === 'POST') {
      posts += 1;
      const comment = JSON.parse(init.body);
      assert.equal(comment.body.startsWith('LUMAFORGE_REVIEW_V1\n```json\n'), true);
      return Response.json({ id: 7001, user: { id: 45896918, login: 'jea27', type: 'User' }, body: comment.body }, { status: 201 });
    }
    throw new Error(`Unexpected mocked request: ${url}`);
  };
  const makeRequest = () => new Request('https://project.test/api/reviews/manual-look/decision', {
    method: 'POST',
    headers: { Origin: 'https://project.test', 'Content-Type': 'application/json', 'X-LumaForge-CSRF': csrf,
      'Idempotency-Key': '55c3c01e-e446-4e5d-8e32-92d466953c27', Cookie: `${SESSION_COOKIE}=${sessionId}` },
    body: JSON.stringify(body),
  });
  const first = await submitDecision({ request: makeRequest(), env, params: { featureId: 'manual-look' } });
  assert.equal(first.status, 200);
  const firstJson = await first.json();
  assert.equal(firstJson.status, 'submitted');
  assert.equal(firstJson.comment.url, 'https://github.com/jea27/Lut_generator/issues/68#issuecomment-7001');
  const replay = await submitDecision({ request: makeRequest(), env, params: { featureId: 'manual-look' } });
  assert.equal(replay.status, 200);
  assert.equal(posts, 1);
});

test('decision route rejects cross-origin and invalid CSRF requests before GitHub writes', async () => {
  await productJsonPromise;
  const db = await sqliteD1();
  activeDbs.add(db);
  const env = { REVIEW_DB: db, SESSION_ENCRYPTION_KEY: secret, GITHUB_APP_CLIENT_ID: 'Iv1.test', GITHUB_APP_CLIENT_SECRET: 'secret', ALLOWED_ORIGIN: 'https://project.test' };
  const sessionId = await createSession(env, { accessToken: 'ghu_example-test-access-token-123456789', refreshToken: 'ghr_example-test-refresh-token-123456789', accessExpiresIn: 3600, refreshExpiresIn: 100000 });
  let githubCalls = 0;
  globalThis.fetch = async () => { githubCalls += 1; throw new Error('must not reach GitHub'); };
  for (const headers of [
    { Origin: 'https://attacker.test', 'X-LumaForge-CSRF': await csrfToken(sessionId, secret) },
    { Origin: 'https://project.test', 'X-LumaForge-CSRF': 'invalid' },
  ]) {
    const response = await submitDecision({
      request: new Request('https://project.test/api/reviews/manual-look/decision', { method: 'POST', headers: {
        ...headers, 'Content-Type': 'application/json', 'Idempotency-Key': 'a9235ba0-5c04-4d69-bc08-33c8bb40b10f', Cookie: `${SESSION_COOKIE}=${sessionId}`,
      }, body: '{}' }),
      env,
      params: { featureId: 'manual-look' },
    });
    assert.equal(response.status, 403);
  }
  assert.equal(githubCalls, 0);
});

test('OAuth start creates one-time PKCE state and a protected host cookie', async () => {
  const db = await sqliteD1();
  activeDbs.add(db);
  const env = { REVIEW_DB: db, SESSION_ENCRYPTION_KEY: secret, GITHUB_APP_CLIENT_ID: 'Iv1.test',
    GITHUB_APP_CLIENT_SECRET: 'server-only-test-secret', ALLOWED_ORIGIN: 'https://project.test' };
  const response = await startLogin({ request: new Request('https://project.test/api/auth/github/start', {
    headers: { 'CF-Connecting-IP': '192.0.2.12' },
  }), env });
  assert.equal(response.status, 303);
  const location = new URL(response.headers.get('Location'));
  assert.equal(location.origin, 'https://github.com');
  assert.equal(location.pathname, '/login/oauth/authorize');
  assert.equal(location.searchParams.get('scope'), 'offline_access');
  assert.equal(location.searchParams.get('login'), 'jea27');
  assert.equal(location.searchParams.get('allow_signup'), 'false');
  assert.equal(location.searchParams.get('code_challenge_method'), 'S256');
  assert.match(location.searchParams.get('code_challenge') || '', /^[A-Za-z0-9_-]{43}$/);
  assert.match(response.headers.get('Set-Cookie'), /__Host-lf_oauth=.*; Path=\/; Secure; HttpOnly; SameSite=Lax/);
  const row = await db.prepare('SELECT * FROM oauth_states').bind().first();
  assert.ok(row);
  assert.equal(row.expires_at-row.created_at, 600);
});

test('GitHub identity is rejected unless login, immutable id and account type all match', async () => {
  let calls = 0;
  globalThis.fetch = async input => {
    calls += 1;
    assert.equal(String(input), 'https://api.github.com/user');
    return Response.json({ id: 45896918, login: 'jea27', type: 'Bot' });
  };
  await assert.rejects(verifyAuthorizedUser('ghu_never-returned-to-client'), error => error.status === 403 && error.code === 'github_user_not_authorized');
  assert.equal(calls, 1);
});

test('a changed review version is rejected before any Issue comment write', async () => {
  await productJsonPromise;
  const db = await sqliteD1();
  activeDbs.add(db);
  const env = { REVIEW_DB: db, SESSION_ENCRYPTION_KEY: secret, GITHUB_APP_CLIENT_ID: 'Iv1.test', GITHUB_APP_CLIENT_SECRET: 'secret', ALLOWED_ORIGIN: 'https://project.test' };
  const sessionId = await createSession(env, { accessToken: 'ghu_example-test-access-token-123456789', refreshToken: 'ghr_example-test-refresh-token-123456789', accessExpiresIn: 3600, refreshExpiresIn: 100000 });
  const csrf = await csrfToken(sessionId, secret);
  const snapshot = testSnapshot();
  let writes = 0;
  globalThis.fetch = async input => {
    const url = String(input);
    if (url.startsWith('https://jea27.github.io/Lut_generator/data/product.json')) return Response.json(snapshot);
    if (url === 'https://api.github.com/user') return Response.json({ id: 45896918, login: 'jea27', type: 'User' });
    if (url === 'https://api.github.com/repos/jea27/Lut_generator/issues/77') return Response.json({ number: 77 });
    if (url.includes('/issues/68/comments')) writes += 1;
    throw new Error(`Unexpected mocked request: ${url}`);
  };
  const feature = snapshot.features.find(item => item.id === 'manual-look');
  const body = { feature: feature.id, revision: feature.review.context.revision, commit: '0'.repeat(40),
    version: feature.review.context.version, decision: 'approve', checklist: feature.checklist.map(item => item.id), notes: '' };
  const response = await submitDecision({
    request: new Request('https://project.test/api/reviews/manual-look/decision', { method: 'POST', headers: {
      Origin: 'https://project.test', 'Content-Type': 'application/json', 'X-LumaForge-CSRF': csrf,
      'Idempotency-Key': '9c6dc869-6cdb-48cb-8c7a-da8f24649650', Cookie: `${SESSION_COOKIE}=${sessionId}`,
    }, body: JSON.stringify(body) }),
    env, params: { featureId: 'manual-look' },
  });
  assert.equal(response.status, 409);
  assert.equal((await response.json()).error, 'review_version_changed');
  assert.equal(writes, 0);
});

test('changes are scoped to one capability, retain notes, and never approve siblings', async () => {
  await productJsonPromise;
  const db = await sqliteD1();
  activeDbs.add(db);
  const env = { REVIEW_DB: db, SESSION_ENCRYPTION_KEY: secret, GITHUB_APP_CLIENT_ID: 'Iv1.test',
    GITHUB_APP_CLIENT_SECRET: 'server-only-test-secret', ALLOWED_ORIGIN: 'https://project.test' };
  const sessionId = await createSession(env, { accessToken: 'ghu_example-test-access-token-123456789',
    refreshToken: 'ghr_example-test-refresh-token-123456789', accessExpiresIn: 3600, refreshExpiresIn: 100000 });
  const csrf = await csrfToken(sessionId, secret);
  const snapshot = testSnapshot();
  const feature = snapshot.features.find(item => item.id === 'glow');
  const body = { feature: 'glow', revision: feature.review.context.revision, commit: feature.review.context.commit,
    version: feature.review.context.version, decision: 'changes', checklist: [], notes: 'Reducir halo alrededor de altas luces.' };
  let postedBody = '';
  globalThis.fetch = async (input, init = {}) => {
    const url = String(input);
    if (url.startsWith('https://jea27.github.io/Lut_generator/data/product.json')) return Response.json(snapshot);
    if (url === 'https://api.github.com/user') return Response.json({ id: 45896918, login: 'jea27', type: 'User' });
    if (url === 'https://api.github.com/repos/jea27/Lut_generator/issues/77') return Response.json({ number: 77 });
    if (url.startsWith('https://api.github.com/repos/jea27/Lut_generator/issues/68/comments?')) return Response.json([]);
    if (url === 'https://api.github.com/repos/jea27/Lut_generator/issues/68/comments' && init.method === 'POST') {
      postedBody = JSON.parse(init.body).body;
      return Response.json({ id: 7002, user: { id: 45896918, login: 'jea27', type: 'User' }, body: postedBody }, { status: 201 });
    }
    throw new Error(`Unexpected mocked request: ${url}`);
  };
  const response = await submitDecision({
    request: new Request('https://project.test/api/reviews/glow/decision', { method: 'POST', headers: {
      Origin: 'https://project.test', 'Content-Type': 'application/json', 'X-LumaForge-CSRF': csrf,
      'Idempotency-Key': '5f220fe7-eac3-40f7-b1f1-36d83f227b3f', Cookie: `${SESSION_COOKIE}=${sessionId}`,
    }, body: JSON.stringify(body) }),
    env, params: { featureId: 'glow' },
  });
  assert.equal(response.status, 200);
  assert.match(postedBody, /"feature": "glow"/);
  assert.match(postedBody, /"decision": "changes"/);
  assert.ok(postedBody.includes('"notes": "Reducir halo alrededor de altas luces."'));
  const row = await db.prepare('SELECT feature_id, decision, issue_number, status FROM review_submissions').bind().first();
  assert.deepEqual({ ...row }, { feature_id: 'glow', decision: 'changes', issue_number: 68, status: 'sent' });
  assert.equal(snapshot.features.find(item => item.id === 'diffusion').review.state, 'pending');
  assert.equal(snapshot.features.find(item => item.id === 'fade').review.state, 'pending');
});

test('GitHub outage fails closed and leaves an idempotent retryable record', async () => {
  await productJsonPromise;
  const db = await sqliteD1();
  activeDbs.add(db);
  const env = { REVIEW_DB: db, SESSION_ENCRYPTION_KEY: secret, GITHUB_APP_CLIENT_ID: 'Iv1.test',
    GITHUB_APP_CLIENT_SECRET: 'server-only-test-secret', ALLOWED_ORIGIN: 'https://project.test' };
  const sessionId = await createSession(env, { accessToken: 'ghu_example-test-access-token-123456789',
    refreshToken: 'ghr_example-test-refresh-token-123456789', accessExpiresIn: 3600, refreshExpiresIn: 100000 });
  const csrf = await csrfToken(sessionId, secret);
  globalThis.fetch = async input => {
    const url = String(input);
    if (url.startsWith('https://api.github.com/')) throw new Error('simulated network outage');
    throw new Error(`Unexpected request: ${url}`);
  };
  const response = await submitDecision({
    request: new Request('https://project.test/api/reviews/glow/decision', { method: 'POST', headers: {
      Origin: 'https://project.test', 'Content-Type': 'application/json', 'X-LumaForge-CSRF': csrf,
      'Idempotency-Key': '8ba61d0f-e6d5-4ab5-baa1-a06bbb0e9454', Cookie: `${SESSION_COOKIE}=${sessionId}`,
    }, body: JSON.stringify({ feature: 'glow', revision: 'a'.repeat(64), commit: 'b'.repeat(40), version: '0.3.0',
      decision: 'approve', checklist: ['a'], notes: '' }) }),
    env, params: { featureId: 'glow' },
  });
  assert.equal(response.status, 503);
  assert.equal((await response.json()).error, 'github_unavailable');
  assert.equal((await db.prepare('SELECT COUNT(*) AS count FROM review_submissions').bind().first()).count, 0);
});
