const CACHE_NAME = "zua-boulot-v1";

const urlsToCache = [
    "/",
    "/offres/",
    "/dashboard/",
    "/static/icon.png",
];

// INSTALLATION
self.addEventListener("install", event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
    );
});

// FETCH (offline mode)
self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                return response || fetch(event.request);
            })
    );
});