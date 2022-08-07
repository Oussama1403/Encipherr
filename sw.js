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

self.addEventListener('fetch', event => {
  if (!event.request.url.startsWith(self.location.origin) || event.request.method !== 'GET') {
    // External request, or POST, ignore
    return void event.respondWith(fetch(event.request));
  }
  if (event.request.url.startsWith(self.location.origin+"/get-file/")) {
    return false;
  }

  event.respondWith(
    // Always try to download from server first
    fetch(event.request).then(response => {
      // When a download is successful cache the result
      /*caches.open(CACHE).then(cache => {
        cache.put(event.request, response)
      });*/
      // And of course display it
      return response.clone();
    }).catch((_err) => {
      // A failure probably means network access issues
      // See if we have a cached version
      return caches.match(event.request).then(cachedResponse => {
        if (cachedResponse) {
          // We did have a cached version, display it
          return cachedResponse;
        }

        // We did not have a cached version, display offline page
        return caches.open(CACHE).then((cache) => {
          const offlineRequest = new Request(offlineFallbackPage);
          return cache.match(offlineRequest);
        });
      });
    })
  );
});

