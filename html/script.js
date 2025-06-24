let tg = window.Telegram.WebApp;
let btn = document.getElementById("openData");
let output = document.getElementById("output");

tg.expand(); // Expand the app to full screen
tg.ready(); // Notify Telegram that the app is ready

btn.addEventListener('click', function(){
   output.innerText = `User ID: ${tg.initDataUnsafe.user.id}`;
});