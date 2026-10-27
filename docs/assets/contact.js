(function(){var f=document.getElementById("cf");if(!f)return;var t=Date.now();
setTimeout(function(){document.getElementById("ready").value="1"},3000);
f.addEventListener("submit",function(ev){if(Date.now()-t<3000||f._honey.value){ev.preventDefault();}});})();
