self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open('movie-rating-app').then((cache) => {
            return cache.addAll([
                '/',
                '../css/base.css',
                '../css/movie.css',
                '../css/movies.css',
                '../css/movie-review.css',
                '../icons/apple-touch-icon.png',
                '../icons/favicon-16x16.png',
                '../icons/favicon-16x16.png',
                '../js/app.js',
                '../icons/192.png',
                '../icons/512.png',
                '../icons/1024.png',
                '../icons/1280x720_screentshot.png',
                '../icons/phone_screenshot.png'
            ]);
        })
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request);
        })
    );
});

// Activate event - Clean up old caches
self.addEventListener('activate', (event) => {
    const cacheWhitelist = [CACHE_NAME];

    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (!cacheWhitelist.includes(cacheName)) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

window.addEventListener('beforeinstallprompt', (e) => {
    // Prevent the mini-infobar from appearing on mobile
    e.preventDefault();
    // Stash the event so it can be triggered later
    deferredPrompt = e;

    // Optionally, show your custom install button here
    document.getElementById('install-button').style.display = 'block';
  });

  document.getElementById('install-button').addEventListener('click', () => {
    // Show the install prompt
    deferredPrompt.prompt();

    deferredPrompt.userChoice.then((choiceResult) => {
      if (choiceResult.outcome === 'accepted') {
        console.log('User accepted the install prompt');
      } else {
        console.log('User dismissed the install prompt');
      }
      deferredPrompt = null;
    });
  });
