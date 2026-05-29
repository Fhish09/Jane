const CACHE_NAME = 'jane-v1';
const ASSETS = ['/', '/index.html', '/icon-192.png', '/icon-512.png'];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
    );
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keys) =>
            Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
        )
    );
    self.clients.claim();
});

self.addEventListener('fetch', (event) => {
    // Don't cache WebSocket or API requests
    if (event.request.url.includes('ws://') || event.request.url.includes('wss://')) return;

    event.respondWith(
        fetch(event.request).catch(() => caches.match(event.request))
    );
});
