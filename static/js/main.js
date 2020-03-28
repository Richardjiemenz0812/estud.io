const divInstall = document.getElementById('installContainer');
const butInstall = document.getElementById('butInstall');

/* Put code here */

/* Only register a service worker if it's supported */
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/static/js/sw.js');
}
i=0
function menu(){
  console.log("yolo")
  if (i == 0) {
    document.getElementById("pp1").style.display = "inline"
    document.getElementById("pp2").style.display = "inline"
    document.getElementById("pp3").style.display = "inline"
    document.getElementById("ul-nav").style.width = "30%"
    document.getElementById("list").style.display = "block"
    i=1
  } else {
    document.getElementById("pp1").style.display = "none"
    document.getElementById("pp2").style.display = "none"
    document.getElementById("pp3").style.display = "none"
    document.getElementById("list").style.display = "none"
    document.getElementById("ul-nav").style.width = "unset"
    i=0
  }
}