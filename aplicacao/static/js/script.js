//timeout alerta
setTimeout(function () {
    document.getElementById("alerta").style.visibility = "hidden";
}, 4000);

setTimeout(function(){ 
    document.getElementById("alerta").style.opacity='0';
}, 1000);

//fechar alerta
function Fechar(){
    document.getElementById("alerta").style.visibility = "hidden";
}

//função toggle menu responsivo
var menu = document.getElementById("menu-lista")
var btn = document.getElementById("menu-hamburger")
btn.addEventListener("click", function () {
    menu.classList.toggle("shown");
});