self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open('movie-rating-app-v1').then((cache) => {
            return cache.addAll([
                '/',
                '/static/css/base.css',
                '/static/icons/apple-touch-icon.png',
                'static/icons/favicon-32x32.png',
                '/static/icons/favicon-16x16.png',
                '/static/css/movie.css',
                '/static/css/movies.css',
                '/static/css/movie-review.css',
                '/static/js/app.js',
                '/static/icons/192.png',
                '/static/icons/512.png',
                '/static/icons/1024.png'
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
