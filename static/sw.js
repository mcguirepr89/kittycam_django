const CACHE_NAME = "kittycam-v1";

const ASSETS_TO_CACHE = [
  "/static/css/app.css",
  "/static/icons/192.png",
  "/static/icons/512.png",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS_TO_CACHE))
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener("fetch", (event) => {
  const request = event.request;

  // ONLY handle GET requests
  if (request.method !== "GET") return;

  // NEVER interfere with HTML navigation
  if (request.mode === "navigate") return;

  event.respondWith(
    caches.match(request).then((cached) => {
      return (
        cached ||
        fetch(request).then((response) => {
          // optionally cache static assets only
          if (request.url.includes("/static/")) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(request, clone);
            });
          }
          return response;
        })
      );
    })
  );
});
