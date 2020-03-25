const files = [
    '/',
    '/profile',
    '/add',
    '/static/css/main.css',
    'https://fonts.googleapis.com/icon?family=Material+Icons',
    'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css',
    '/static/bg.jpg'
]

self.addEventListener("install",event =>{
    console.log("yolo")
    caches.open("cache").then(cache =>{
        cache.addAll(files)
    })
})

self.addEventListener('activate', (event) => {
    console.log('👷', 'activate', event);
    return self.clients.claim();
  });

  self.addEventListener('fetch', function(event) {
    console.log("fetch")
    event.respondWith(
        caches.match(event.request)
            .then(response => response || fetch(event.request))
            .catch(() =>{
                if (event.request.mode == 'navigate'){
                    return caches.match("/")
                }
            })
    )
  });