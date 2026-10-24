// Dream Ball service worker: app shell precache + runtime cache for fonts and pixel art.
const VERSION = 'dreamball-app-v4';
const SHELL = ['./', './index.html', './manifest.webmanifest?v=2', './icons/icon-192.png', './icons/icon-512.png', './icons/maskable-512.png', './icons/apple-touch-icon.png', './icons/favicon.png'];

self.addEventListener('install', e => {
  e.waitUntil((async () => {
    const c = await caches.open(VERSION);
    await c.addAll(SHELL);
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', e => {
  e.waitUntil((async () => {
    for (const k of await caches.keys()) if (k !== VERSION) await caches.delete(k);
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (req.mode === 'navigate') {
    e.respondWith((async () => {
      try {
        const res = await fetch(req);
        const c = await caches.open(VERSION); c.put('./index.html', res.clone());
        return res;
      } catch (err) {
        return (await caches.match('./index.html')) || (await caches.match('./'));
      }
    })());
    return;
  }
  if (url.hostname.endsWith('cloudfront.net') && /\.mp4($|\?)/.test(url.pathname)) return;   // let video stream normally
  const cdn = url.hostname === 'cdnjs.cloudflare.com' || url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com' || url.hostname.endsWith('cloudfront.net');
  if (url.origin === self.location.origin || cdn) {
    e.respondWith((async () => {
      const hit = await caches.match(req);
      const net = fetch(req).then(res => {
        if (res && (res.status === 200 || res.type === 'opaque')) caches.open(VERSION).then(c => c.put(req, res.clone())).catch(() => {});
        return res;
      }).catch(() => null);
      return hit || (await net) || new Response('', {status: 504});
    })());
  }
});
