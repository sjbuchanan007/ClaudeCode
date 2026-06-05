/* The Valuator — service worker for offline support.
 *
 * Strategy:
 *   - Network-first for the page (index.html) so online users always get the
 *     latest version, with a cache fallback when offline.
 *   - Cache-first for static assets (icons, logo, manifest).
 *   - Cross-origin requests (analytics, CDNs) are left untouched — they pass
 *     straight to the network and simply fail silently when offline.
 *
 * Bump CACHE when the asset list or strategy changes to retire old caches.
 */
var CACHE = "valuator-v1";
var CORE = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./logo-mark.png",
  "./icon-180.png",
  "./icon-192.png",
  "./icon-512.png"
];

self.addEventListener("install", function (e) {
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then(function (c) { return c.addAll(CORE); }));
});

self.addEventListener("activate", function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.map(function (k) {
        if (k !== CACHE) return caches.delete(k);
      }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function (e) {
  var req = e.request;
  if (req.method !== "GET") return;

  var url = new URL(req.url);
  // Only handle our own files; let analytics/external links go to the network.
  if (url.origin !== self.location.origin) return;

  var isPage = req.mode === "navigate" ||
    (req.headers.get("accept") || "").indexOf("text/html") !== -1;

  if (isPage) {
    // Network-first: freshest page when online, cached page when offline.
    e.respondWith(
      fetch(req).then(function (res) {
        var copy = res.clone();
        caches.open(CACHE).then(function (c) { c.put("./index.html", copy); });
        return res;
      }).catch(function () {
        return caches.match("./index.html").then(function (r) {
          return r || caches.match("./");
        });
      })
    );
    return;
  }

  // Cache-first for static assets.
  e.respondWith(
    caches.match(req).then(function (cached) {
      return cached || fetch(req).then(function (res) {
        var copy = res.clone();
        caches.open(CACHE).then(function (c) { c.put(req, copy); });
        return res;
      });
    })
  );
});
