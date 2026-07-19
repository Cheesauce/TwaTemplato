// TwaTemplato service worker — offline app shell.
// Bump CACHE version on any asset change to force clients to update.
const CACHE = 'twatemplato-v55';
const ASSETS = [
  './',
  './index.html',
  './style.css',
  './script.js',
  './icon-192.png',
  './icon-512.png',
  './apple-touch-icon.png',
  './favicon.ico',
  './favicon-16.png',
  './favicon-32.png',
  'https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.12.0/html2pdf.bundle.min.js'
];

self.addEventListener('install', event => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE).then(c => Promise.allSettled(ASSETS.map(a => c.add(a))))
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;
  // Network-first for the app's own HTML/CSS/JS so updates land quickly;
  // cache-first for everything else (icons, CDN lib) for speed & offline.
  const isAppShell = /\.(html|css|js)(\?|$)/.test(req.url) && req.url.indexOf('cloudflare') === -1;
  if (isAppShell) {
    event.respondWith(
      fetch(req).then(res => {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(req, copy)).catch(() => {});
        return res;
      }).catch(() => caches.match(req))
    );
  } else {
    event.respondWith(
      caches.match(req).then(hit => hit || fetch(req).then(res => {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(req, copy)).catch(() => {});
        return res;
      }).catch(() => hit))
    );
  }
});
