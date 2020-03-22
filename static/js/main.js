/*window.addEventListener('load', () => {
    regissw()
})
*/



function delcookie(){
    document.cookie = "user" + '=; Max-Age=0'
}

function menu(){
    prompt("yolo")
}

function regissw(){
    navigator.serviceWorker.register("/sw.js")
    install()
}
/*
function install(){
    navigator.serviceWorker.register('./sw.js').then(function(registration) {
        if (registration.installing) {
            // Service Worker is Installing
        }
    })
}
*/
