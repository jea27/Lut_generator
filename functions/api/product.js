import { PRODUCT_SNAPSHOT_URL, validateSnapshotShape } from '../_lib/product.mjs';
import { jsonResponse } from '../_lib/security.mjs';

export async function onRequestGet() {
  try {
    const url = new URL(PRODUCT_SNAPSHOT_URL);
    url.searchParams.set('_', String(Date.now()));
    const response = await fetch(url, {
      headers: { Accept: 'application/json' },
      cache: 'no-store',
      redirect: 'error',
      signal: AbortSignal.timeout(10000),
    });
    if (!response.ok || response.headers.get('Content-Type')?.toLowerCase().split(';')[0] !== 'application/json') {
      return jsonResponse(503, { error: 'product_unavailable' });
    }
    const text = await response.text();
    if (new TextEncoder().encode(text).byteLength > 2 * 1024 * 1024) return jsonResponse(503, { error: 'product_unavailable' });
    const data = JSON.parse(text);
    if (!validateSnapshotShape(data)) return jsonResponse(503, { error: 'product_unavailable' });
    return new Response(text, {
      status: 200,
      headers: {
        'Cache-Control': 'no-store, max-age=0',
        'Content-Type': 'application/json; charset=utf-8',
        'Referrer-Policy': 'no-referrer',
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
      },
    });
  } catch {
    return jsonResponse(503, { error: 'product_unavailable' });
  }
}
