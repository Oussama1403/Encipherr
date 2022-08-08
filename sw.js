// This is the "Offline page" service worker

importScripts('https://storage.googleapis.com/workbox-cdn/releases/5.1.2/workbox-sw.js');


const CACHE = "1.0";

// TODO: replace the following with the correct offline fallback page i.e.: const offlineFallbackPage = "offline.html";
const assets = ["/offline","/static/offline/style.css","/static/offline/modules.py"];
const offlineFallbackPage = "/offline"
self.addEventListener("message", (event) => {
  if (event.data && event.data.type === "SKIP_WAITING") {
    self.skipWaiting();
  }
});

self.addEventListener('install', async (event) => {
  event.waitUntil(
    caches.open(CACHE)
      .then((cache) => cache.addAll(assets))
  );
});

if (workbox.navigationPreload.isSupported()) {
  workbox.navigationPreload.enable();
}


addEventListener('fetch', (event) => {
    const { request } = event;
  
    // Always bypass for range requests, due to browser bugs
    if (request.headers.has('range')) return;
    event.respondWith(async function() {
      // Try to get from the cache:
      const cachedResponse = await caches.match(request);
      if (cachedResponse) return cachedResponse;
  
      try {
        // See https://developers.google.com/web/updates/2017/02/navigation-preload#using_the_preloaded_response
        const response = await event.preloadResponse;
        if (response) return response;
  
        // Otherwise, get from the network
        return await fetch(request);
      } catch (err) {
        // If this was a navigation, show the offline page:
        if (request.mode === 'navigate') {
          return caches.match('/offline');
        }
  
        // Otherwise throw
        throw err;
      }
    }());
  });