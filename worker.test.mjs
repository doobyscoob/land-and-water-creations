import test from 'node:test';
import assert from 'node:assert/strict';
import worker from './worker.mjs';

for (const origin of ['http://landandwatercreations.com', 'http://www.landandwatercreations.com', 'https://www.landandwatercreations.com']) {
  for (const path of ['/', '/water-features', '/projects/orangedale-pond?utm_source=test&x=a%2Fb', '/css/base.css']) {
    test(`redirect ${origin}${path}`, async () => {
      const response = await worker.fetch(new Request(origin + path), {ASSETS: {fetch() {throw Error('Should redirect before assets');}}});
      assert.equal(response.status, 308);
      assert.equal(response.headers.get('location'), 'https://landandwatercreations.com' + path);
    });
  }
}
for (const origin of ['https://landandwatercreations.com', 'https://preview.workers.dev', 'http://localhost:8787']) {
  test(`pass through ${origin}`, async () => {
    const request = new Request(origin + '/contact-us');
    const expected = new Response('asset', {status: 200});
    const response = await worker.fetch(request, {ASSETS: {fetch(r) {assert.equal(r, request); return expected;}}});
    assert.equal(response, expected);
  });
}
