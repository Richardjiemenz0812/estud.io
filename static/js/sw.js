const cacheName = 'estud.io-v1'
const staticAssets = [
    "/static/css/main.css",
    "/static/js/main.js"]

self.addEventListener('install', event => {
    const cache = caches.open(cacheName)
    cache.addAll(staticAssets)
});

self.addEventListener('activate', event => {
    self.clients.claim()
});
