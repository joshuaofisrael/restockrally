(function(){var L=document.getElementById("rel-list");if(!L)return;var rows=[].slice.call(L.children);
function g(i){return document.getElementById(i)}
function run(){var b=g("f-brand").value,f=g("f-from").value,t=g("f-to").value,p=g("f-price").value,s=g("f-sort").value,n=0;
rows.sort(function(a,c){return s==="price"?a.dataset.price-c.dataset.price:(a.dataset.date<c.dataset.date?-1:a.dataset.date>c.dataset.date?1:0)});
rows.forEach(function(r){var ok=(!b||r.dataset.brand===b)&&(!f||r.dataset.date>=f)&&(!t||r.dataset.date<=t)&&(!p||+r.dataset.price<=+p);r.hidden=!ok;if(ok)n++;L.appendChild(r)});
g("count").textContent=n+(n===1?" release":" releases");}
["f-brand","f-from","f-to","f-price","f-sort"].forEach(function(i){g(i).addEventListener("change",run)});})();
