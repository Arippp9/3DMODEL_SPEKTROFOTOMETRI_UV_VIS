"""Komponen 3D interaktif (Three.js) untuk st.components.v1.html."""

VIEWER_HTML = r"""
<!DOCTYPE html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box}
body{margin:0;font-family:Inter,Segoe UI,Arial,sans-serif;background:#0a1f44;overflow:hidden}
#wrap{position:relative;width:100%;height:640px;background:radial-gradient(circle at 50% 30%,#16396f,#0a1f44 70%);border-radius:16px;overflow:hidden}
canvas{display:block;width:100%;height:100%;touch-action:none;cursor:grab}
#bar{position:absolute;left:10px;top:10px;display:flex;flex-wrap:wrap;gap:6px;max-width:68%}
#bar button{background:rgba(255,255,255,.12);color:#fff;border:1px solid rgba(255,255,255,.25);border-radius:999px;padding:6px 12px;font-size:12px;cursor:pointer;backdrop-filter:blur(6px)}
#bar button:hover,#bar button.on{background:#06b6d4;border-color:#06b6d4;color:#042}
#info{position:absolute;right:10px;top:10px;width:260px;max-height:92%;overflow:auto;background:rgba(255,255,255,.96);border-radius:14px;padding:14px;font-size:13px;color:#0a1f44;box-shadow:0 8px 30px rgba(0,0,0,.3)}
#info h3{margin:0 0 6px;font-size:16px;color:#0a1f44}
#info .tag{display:inline-block;background:#e0f7fb;color:#0e7490;border-radius:8px;padding:2px 8px;font-size:11px;margin-bottom:6px}
#info p{margin:6px 0;line-height:1.45}
#label{position:absolute;pointer-events:none;background:#06b6d4;color:#031a2b;font-weight:700;font-size:13px;padding:4px 10px;border-radius:8px;transform:translate(-50%,-140%);display:none;white-space:nowrap}
#hint{position:absolute;left:12px;bottom:10px;color:#9fb7d9;font-size:11px}
#msg{position:absolute;inset:0;display:none;align-items:center;justify-content:center;color:#fff;text-align:center;padding:30px;font-size:14px}
@media(max-width:640px){#info{top:auto;bottom:0;right:0;left:0;width:auto;max-height:42%;border-radius:14px 14px 0 0}#bar{max-width:100%}#hint{display:none}}
</style></head><body>
<div id="wrap">
 <div id="bar">
  <button onclick="setView('iso')">Isometrik</button><button onclick="setView('front')">Depan</button>
  <button onclick="setView('top')">Atas</button><button onclick="setView('side')">Samping</button>
  <button onclick="resetView()">⟲ Reset</button>
  <button id="bLid" onclick="toggleLid()">Buka Kompartemen Kuvet</button>
  <button id="bPath" onclick="togglePath()">Lihat Jalur Cahaya</button>
  <button id="bX" class="on" onclick="toggleX()">Mode Tembus</button>
 </div>
 <div id="info"><span class="tag">Klik komponen</span><h3>Pilih sebuah komponen</h3><p>Klik bagian mana pun pada model untuk melihat fungsinya. Seret mouse untuk memutar, scroll untuk zoom.</p></div>
 <div id="label"></div>
 <div id="hint">Visualisasi edukasi — komponen internal bukan gambaran pasti instrumen komersial tertentu.</div>
 <div id="msg"></div>
</div>
<script>
var INFO={
 body:["Bodi Instrumen","Rangka","Casing menopang seluruh komponen optik dan elektronik, melindungi dari cahaya luar (stray light) dan debu. Pada mode tembus, bagian dalam terlihat."],
 screen:["Layar Digital","Antarmuka","Menampilkan panjang gelombang, absorbansi, %T, dan status pengukuran. Nilai pada layar ini hanya ilustrasi."],
 panel:["Panel Kontrol","Sistem kontrol","Tombol untuk memilih λ, melakukan blanko (autozero), memulai pengukuran, dan mengatur mode (A, %T, konsentrasi)."],
 lamp:["Sumber Cahaya","Optik","Lampu deuterium untuk UV (±190–350 nm) dan lampu tungsten/halogen untuk cahaya tampak (±350–1100 nm). Menghasilkan radiasi polikromatik kontinu."],
 mono:["Monokromator","Optik","Berisi kisi difraksi atau prisma yang menguraikan cahaya polikromatik dan memilih satu panjang gelombang sempit yang akan melewati sampel."],
 slit:["Celah Optik (Slit)","Optik","Membatasi lebar berkas dan lebar pita spektral. Celah sempit meningkatkan resolusi tetapi mengurangi intensitas cahaya."],
 comp:["Kompartemen Sampel","Sampel","Ruang tertutup tempat kuvet diletakkan sehingga berkas melewati sampel dengan lintasan tetap dan terlindung dari cahaya luar."],
 cuv:["Kuvet","Sampel","Wadah sampel berlintasan optik b (umumnya 1 cm). Kuvet kuarsa dipakai untuk UV; kaca/plastik hanya untuk daerah tampak. Pegang pada sisi buram."],
 det:["Detektor","Elektronik","Fotodioda atau tabung pengganda foton (PMT) yang mengubah intensitas cahaya yang diteruskan (I) menjadi sinyal listrik."],
 lid:["Tutup Kompartemen","Sampel","Dibuka untuk memasang kuvet dan ditutup saat pengukuran agar cahaya ruangan tidak mengganggu detektor."]
};
var scene,camera,renderer,pick=[],parts={},sel=null,lidOpen=false,pathOn=false,xray=true,lid,beams,parts_p=[];
var V={iso:[0.7,1.1,12],front:[0,1.45,11],top:[0,0.05,12],side:[1.5708,1.45,11]};
var cur={th:.7,ph:1.1,r:12},goal={th:.7,ph:1.1,r:12},tgt;
function show(t){var m=document.getElementById('msg');m.style.display='flex';m.innerHTML=t}
function load(urls,i){
 if(i>=urls.length){show('Model 3D tidak dapat dimuat (Three.js gagal diunduh dari CDN).<br>Periksa koneksi internet lalu muat ulang halaman. Daftar komponen: sumber cahaya → monokromator → celah → kuvet → detektor → pengolah sinyal → layar.');return}
 var s=document.createElement('script');s.src=urls[i];s.onload=function(){try{init()}catch(e){show('Kesalahan inisialisasi 3D: '+e.message)}};
 s.onerror=function(){load(urls,i+1)};document.head.appendChild(s);
}
load(['https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js','https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js'],0);

function init(){
 var wrap=document.getElementById('wrap');
 var test=document.createElement('canvas');
 if(!(test.getContext('webgl')||test.getContext('experimental-webgl'))){show('Browser Anda tidak mendukung WebGL sehingga model 3D tidak dapat ditampilkan.');return}
 scene=new THREE.Scene();
 camera=new THREE.PerspectiveCamera(40,wrap.clientWidth/wrap.clientHeight,.1,100);
 renderer=new THREE.WebGLRenderer({antialias:true,alpha:true});
 renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.setSize(wrap.clientWidth,wrap.clientHeight);
 wrap.insertBefore(renderer.domElement,wrap.firstChild);
 tgt=new THREE.Vector3(.2,.6,0);
 scene.add(new THREE.AmbientLight(0xffffff,.75));
 var d=new THREE.DirectionalLight(0xffffff,.9);d.position.set(5,9,7);scene.add(d);
 var d2=new THREE.DirectionalLight(0x66ddee,.4);d2.position.set(-6,3,-5);scene.add(d2);
 var M=function(c,o){return new THREE.MeshStandardMaterial(Object.assign({color:c,roughness:.45,metalness:.25},o||{}))};
 function add(id,geo,mat,x,y,z,parent){var m=new THREE.Mesh(geo,mat);m.position.set(x,y,z);m.userData.id=id;m.userData.base=mat.emissive.getHex();m.userData.bi=mat.emissiveIntensity;(parent||scene).add(m);pick.push(m);(parts[id]=parts[id]||[]).push(m);return m}
 var B=function(w,h,l){return new THREE.BoxGeometry(w,h,l)};
 var C=function(r,h,s){return new THREE.CylinderGeometry(r,r,h,s||32)};
 // alas
 var floor=new THREE.Mesh(new THREE.CircleGeometry(9,64),new THREE.MeshStandardMaterial({color:0x10305f,roughness:.9}));floor.rotation.x=-Math.PI/2;scene.add(floor);
 // bodi
 add('body',B(7.2,1.3,2.6),M(0xe8eef7,{transparent:true,opacity:.38,metalness:.1}),0,.65,0);
 add('body',B(7.4,.12,2.8),M(0x1d3557),0,.06,0);
 // layar (canvas texture)
 var cv=document.createElement('canvas');cv.width=256;cv.height=128;var g=cv.getContext('2d');
 g.fillStyle='#052b3a';g.fillRect(0,0,256,128);g.fillStyle='#22d3ee';g.font='bold 22px monospace';
 g.fillText('λ = 540 nm',16,36);g.fillText('A = 0.452',16,72);g.font='14px monospace';g.fillText('%T = 35.3   SIMULASI',16,108);
 var tex=new THREE.CanvasTexture(cv);
 var sc=add('screen',B(1.7,.8,.06),M(0x0b3b4d,{emissive:0xffffff,emissiveIntensity:.9,emissiveMap:tex,map:tex}),-1.9,.75,1.33);
 sc.userData.base=sc.material.emissive.getHex();
 add('panel',B(2.0,.8,.06),M(0x24324d),1.7,.75,1.33);
 for(var i=0;i<4;i++)add('panel',C(.1,.08,20),M(i==3?0x06b6d4:0xcbd5e1),.9+i*.5,.9,1.4).rotation.x=Math.PI/2;
 for(var j=0;j<3;j++)add('panel',C(.09,.08,20),M(0x94a3b8),1.15+j*.5,.55,1.4).rotation.x=Math.PI/2;
 // lampu
 add('lamp',C(.34,.9,32),M(0x555f73),-2.9,.5,0).rotation.z=Math.PI/2;
 add('lamp',new THREE.SphereGeometry(.2,24,24),M(0xffc94d,{emissive:0xffa000,emissiveIntensity:.9}),-2.35,.5,0);
 // monokromator
 add('mono',B(1.0,.9,1.0),M(0x3b4a6b,{transparent:true,opacity:.85}),-1.5,.5,0);
 add('mono',C(.3,.15,40),M(0xc0c9d8,{metalness:.8,roughness:.2}),-1.5,.5,0).rotation.z=.5;
 // celah
 add('slit',B(.06,.35,.7),M(0x111827),-.6,.2,0);add('slit',B(.06,.35,.7),M(0x111827),-.6,.8,0);
 // kompartemen + kuvet
 add('comp',B(1.5,1.0,1.3),M(0x1f2a44,{transparent:true,opacity:.55}),.7,.5,0);
 add('cuv',B(.34,.9,.34),M(0xbfeaff,{transparent:true,opacity:.35,roughness:.05}),.7,.5,0);
 add('cuv',B(.28,.6,.28),M(0x22d3ee,{transparent:true,opacity:.75,emissive:0x0891b2,emissiveIntensity:.25}),.7,.35,0);
 var pv=new THREE.Group();pv.position.set(.7,1.36,-.65);scene.add(pv);lid=pv;
 add('lid',B(1.5,.1,1.3),M(0x2b3a5c),0,0,.65,pv);
 // detektor
 add('det',B(.7,.7,.7),M(0x334155),2.8,.5,0);
 add('det',C(.22,.15,32),M(0x10b981,{emissive:0x047857,emissiveIntensity:.5}),2.4,.5,0).rotation.z=Math.PI/2;
 // jalur cahaya
 beams=new THREE.Group();beams.visible=false;scene.add(beams);
 function beam(x1,x2,c,o){var m=new THREE.Mesh(C(.045,x2-x1,12),new THREE.MeshBasicMaterial({color:c,transparent:true,opacity:o}));m.rotation.z=Math.PI/2;m.position.set((x1+x2)/2,.5,0);beams.add(m)}
 beam(-2.2,-1.95,0xfff1b0,.8);beam(-1.05,.53,0x22d3ee,.8);beam(.87,2.38,0x22d3ee,.45);
 for(var k=0;k<14;k++){var p=new THREE.Mesh(new THREE.SphereGeometry(.07,10,10),new THREE.MeshBasicMaterial({color:0xffffff}));p.userData.k=k;beams.add(p);parts_p.push(p)}
 // event
 var el=renderer.domElement,down=null;
 el.addEventListener('pointerdown',function(e){down={x:e.clientX,y:e.clientY,moved:0};el.setPointerCapture(e.pointerId);el.style.cursor='grabbing'});
 el.addEventListener('pointermove',function(e){if(!down)return;var dx=e.clientX-down.x,dy=e.clientY-down.y;down.moved+=Math.abs(dx)+Math.abs(dy);down.x=e.clientX;down.y=e.clientY;
  goal.th-=dx*.008;goal.ph=Math.min(3.0,Math.max(.1,goal.ph-dy*.008));cur.th=goal.th;cur.ph=goal.ph});
 el.addEventListener('pointerup',function(e){el.style.cursor='grab';if(down&&down.moved<6)doPick(e);down=null});
 el.addEventListener('wheel',function(e){e.preventDefault();goal.r=Math.min(22,Math.max(4,goal.r*(1+e.deltaY*.001)))},{passive:false});
 addEventListener('resize',function(){camera.aspect=wrap.clientWidth/wrap.clientHeight;camera.updateProjectionMatrix();renderer.setSize(wrap.clientWidth,wrap.clientHeight)});
 setXray();animate();
}
function doPick(e){
 var r=renderer.domElement.getBoundingClientRect(),v=new THREE.Vector2(((e.clientX-r.left)/r.width)*2-1,-((e.clientY-r.top)/r.height)*2+1);
 var rc=new THREE.Raycaster();rc.setFromCamera(v,camera);var hits=rc.intersectObjects(pick,false),h=null;
 for(var i=0;i<hits.length;i++){if(hits[i].object.userData.id!=='body'){h=hits[i];break}}
 if(!h&&hits.length)h=hits[0];
 select(h?h.object.userData.id:null);
}
function select(id){
 sel=id;
 for(var k in parts)parts[k].forEach(function(m){m.material.emissive.setHex(k===id?0x0891b2:m.userData.base);m.material.emissiveIntensity=(k===id)?.7:m.userData.bi});
 var i=document.getElementById('info'),l=document.getElementById('label');
 if(!id||!INFO[id]){l.style.display='none';return}
 var f=INFO[id];i.innerHTML='<span class="tag">'+f[1]+'</span><h3>'+f[0]+'</h3><p>'+f[2]+'</p>';
 l.textContent=f[0];l.style.display='block';
}
function setView(n){var v=V[n];goal.th=v[0];goal.ph=v[1];goal.r=v[2]}
function resetView(){setView('iso');select(null);if(lidOpen)toggleLid();if(pathOn)togglePath()}
function toggleLid(){lidOpen=!lidOpen;document.getElementById('bLid').textContent=lidOpen?'Tutup Kompartemen Kuvet':'Buka Kompartemen Kuvet'}
function togglePath(){pathOn=!pathOn;beams.visible=pathOn;document.getElementById('bPath').classList.toggle('on',pathOn)}
function toggleX(){xray=!xray;document.getElementById('bX').classList.toggle('on',xray);setXray()}
function setXray(){parts.body[0].material.opacity=xray?.38:.95}
function animate(){
 requestAnimationFrame(animate);
 var t=performance.now()/1000;
 if(goal.th-cur.th>3.14||cur.th-goal.th>3.14){cur.th=goal.th}
 cur.th+=(goal.th-cur.th)*.12;cur.ph+=(goal.ph-cur.ph)*.12;cur.r+=(goal.r-cur.r)*.12;
 camera.position.set(tgt.x+cur.r*Math.sin(cur.ph)*Math.sin(cur.th),tgt.y+cur.r*Math.cos(cur.ph),tgt.z+cur.r*Math.sin(cur.ph)*Math.cos(cur.th));
 camera.lookAt(tgt);
 var lt=lidOpen?-1.9:0;lid.rotation.x+=(lt-lid.rotation.x)*.1;
 if(pathOn)parts_p.forEach(function(p){var u=((t*.18+p.userData.k/14)%1);var x=-2.35+u*4.7;p.position.set(x,.5,0);p.material.color.setHex(x<-1.05?0xfff1b0:0x67e8f9);p.visible=true});
 var l=document.getElementById('label');
 if(sel&&parts[sel]){var b=new THREE.Box3().setFromObject(parts[sel][0]),c=new THREE.Vector3();b.getCenter(c);c.y=b.max.y;c.project(camera);
  var w=renderer.domElement.clientWidth,h=renderer.domElement.clientHeight;l.style.left=((c.x+1)/2*w)+'px';l.style.top=((1-c.y)/2*h)+'px'}
 renderer.render(scene,camera);
}
</script></body></html>
"""
