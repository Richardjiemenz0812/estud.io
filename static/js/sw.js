const files = [
    '/',
    '/profile',
    '/add',
    '/static/css/main.css',
    'https://fonts.googleapis.com/icon?family=Material+Icons',
    'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css',
    '/static/bg.jpg'
]

self.addEventListener("install",evt =>{
    caches.open("cache").then(cache =>{
        cache.addAll(files)
    })
})

self.addEventListener("fetch",evt =>{
    evt.respondWith(
        caches.match(evt.request).then(cachesRes =>{
            return cachesRes || fetch(evt.request)
        })
    )
})