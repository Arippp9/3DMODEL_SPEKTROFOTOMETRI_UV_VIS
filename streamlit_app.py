import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import math

st.set_page_config(
    page_title="UV-Vis Explorer",
    page_icon="🔬",
    layout="wide"
)

# =========================
# DESAIN WEBSITE
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

.stApp {
    background: linear-gradient(180deg,#f4f7fb,#eaf1f9);
    font-family: Inter, sans-serif;
}
.block-container {
    max-width: 1150px;
    padding-top: 2rem;
}
.hero {
    padding: 35px;
    border-radius: 24px;
    background: linear-gradient(135deg,#0a1f44,#12366b,#0e7490);
    color: white;
}
.hero h1 {
    color: white;
    font-size: 2.5rem;
    font-weight: 800;
}
.hero p {
    color: #dbeafe;
    line-height: 1.7;
}
.card {
    background: white;
    border: 1px solid #dbe4ef;
    padding: 22px;
    border-radius: 18px;
    margin-bottom: 12px;
    box-shadow: 0 5px 18px #0a1f4410;
}
.section-title {
    font-size: 1.5rem;
    font-weight: 800;
    color: #0a1f44;
    border-left: 5px solid #06b6d4;
    padding-left: 12px;
    margin: 24px 0 16px;
}
.note {
    background: #ecfeff;
    border: 1px solid #a5f3fc;
    border-radius: 12px;
    padding: 15px;
    color: #164e63;
}
.stButton button {
    border-radius: 10px;
    font-weight: 600;
}
footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)


# =========================
# FUNGSI PERHITUNGAN
# =========================
def hitung_absorbansi(T):
    if not math.isfinite(T) or T <= 0 or T > 1:
        raise ValueError("Transmitansi harus lebih dari 0 sampai 1.")
    return -math.log10(T)


def hitung_transmitansi(A):
    if not math.isfinite(A) or A < 0:
        raise ValueError("Absorbansi tidak boleh negatif.")
    return 10 ** (-A)


def hitung_konsentrasi(A, epsilon, b):
    if epsilon <= 0 or b <= 0:
        raise ValueError("Nilai epsilon dan panjang lintasan harus lebih dari 0.")
    if A < 0:
        raise ValueError("Absorbansi tidak boleh negatif.")
    return A / (epsilon * b)


# =========================
# MODEL 3D SPEKTROFOTOMETER
# =========================
MODEL_3D = r"""
<div id="uvvis" style="height:590px;width:100%;position:relative;background:#eaf2fb;border-radius:18px;overflow:hidden;font-family:Arial">
<div style="position:absolute;z-index:2;top:10px;left:10px;background:white;padding:9px;border-radius:8px;color:#0a1f44">
Model 3D UV-Vis
</div>
<div style="position:absolute;z-index:2;top:10px;right:10px;display:flex;gap:5px;flex-wrap:wrap;justify-content:flex-end;max-width:70%">
<button onclick="toggleRotation()" id="rotationButton">⟳ Putar otomatis</button>
<button onclick="toggleLid()">Buka/tutup kuvet</button>
<button onclick="toggleBeam()" id="beamButton">Jalur cahaya</button>
<button onclick="resetModel()">Reset</button>
</div>
<div style="position:absolute;z-index:2;bottom:10px;left:10px;max-width:290px;background:#ffffffed;border-radius:10px;padding:12px;color:#0a1f44">
<b id="partTitle">Pilih komponen</b>
<div id="partInfo" style="font-size:13px;line-height:1.5;margin-top:5px">Seret model untuk memutar. Gunakan scroll untuk zoom dan klik komponen untuk mengetahui fungsinya.</div>
</div>
</div>

<style>
#uvvis button {
background:white;border:1px solid #cbd5e1;border-radius:8px;
padding:8px;color:#0a1f44;cursor:pointer;font-size:12px
}
#uvvis button:hover {background:#cffafe}
</style>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
(function(){
const root=document.getElementById('uvvis');
if(!window.THREE){
root.innerHTML='Model 3D tidak dapat dimuat. Periksa koneksi internet.';
return;
}

const scene=new THREE.Scene();
scene.background=new THREE.Color('#eaf2fb');

const camera=new THREE.PerspectiveCamera(45,root.clientWidth/root.clientHeight,.1,100);
let theta=.7,phi=1.0,radius=9,auto=false,lidOpen=false,beamOn=false;
const renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setPixelRatio(Math.min(window.devicePixelRatio||1,2));
renderer.setSize(root.clientWidth,root.clientHeight);
renderer.domElement.style.width='100%';
renderer.domElement.style.height='100%';
root.insertBefore(renderer.domElement,root.children[0]);

scene.add(new THREE.HemisphereLight(0xffffff,0x718096,2));
const light=new THREE.DirectionalLight(0xffffff,2);
light.position.set(5,8,6);
scene.add(light);

const floor=new THREE.Mesh(
new THREE.PlaneGeometry(100,100),
new THREE.MeshStandardMaterial({color:'#dce7f3'})
);
floor.rotation.x=-Math.PI/2;
floor.position.y=-.04;
scene.add(floor);

const grid=new THREE.GridHelper(20,40,0xa9bed5,0xd0dce9);
grid.position.y=-.02;
scene.add(grid);

const machine=new THREE.Group();
scene.add(machine);
const clickable=[];

function mat(color,transparent=false,opacity=1){
return new THREE.MeshStandardMaterial({
color,roughness:.4,metalness:.12,transparent,opacity
});
}

function box(name,pos,size,color,description){
const obj=new THREE.Mesh(
new THREE.BoxGeometry(...size),mat(color)
);
obj.position.set(...pos);
obj.userData={name,description};
machine.add(obj);
clickable.push(obj);
return obj;
}

box('Bodi instrumen',[0,1,0],[4.8,1.7,3],'#e5eaf0',
'Bodi instrumen melindungi sistem optik dan elektronik spektrofotometer.');

box('Layar digital',[-1.3,1.35,1.52],[1.3,.65,.05],'#082f49',
'Layar digital menampilkan panjang gelombang dan hasil pengukuran.');

box('Panel kontrol',[1,1.3,1.53],[1.3,.7,.05],'#334155',
'Panel kontrol digunakan untuk mengatur parameter pengukuran.');

box('Sumber cahaya',[-1.65,.55,-.65],[.55,.5,.55],'#fbbf24',
'Sumber cahaya menghasilkan radiasi ultraviolet dan cahaya tampak.');

box('Monokromator',[-.65,.55,-.65],[.55,.55,.55],'#64748b',
'Monokromator memilih panjang gelombang tertentu dari cahaya sumber.');

box('Detektor',[1.45,.55,-.65],[.5,.5,.5],'#34d399',
'Detektor mengubah cahaya yang diterima menjadi sinyal listrik.');

const lid=new THREE.Group();
lid.position.set(.35,1.95,-.15);
machine.add(lid);
const lidMesh=new THREE.Mesh(
new THREE.BoxGeometry(1.4,.16,1.2),mat('#94a3b8')
);
lidMesh.position.set(0,.08,0);
lid.add(lidMesh);
lid.userData={name:'Tutup kompartemen',description:'Tutup melindungi tempat sampel dari cahaya luar.'};
clickable.push(lidMesh);

box('Kuvet',[.35,2.25,-.15],[.32,.45,.32],'#67e8f9',
'Kuvet adalah wadah sampel. Panjang lintasan optik yang umum digunakan adalah 1 cm.');

box('Isi sampel',[.35,2.23,-.15],[.27,.30,.27],'#8b5cf6',
'Sampel menyerap sebagian cahaya pada panjang gelombang tertentu.');

const beamGroup=new THREE.Group();
machine.add(beamGroup);

function addBeam(a,b,color){
const start=new THREE.Vector3(...a);
const end=new THREE.Vector3(...b);
const dir=new THREE.Vector3().subVectors(end,start);
const obj=new THREE.Mesh(
new THREE.CylinderGeometry(.035,.035,dir.length(),12),
mat(color,true,.9)
);
obj.position.copy(start).add(end).multiplyScalar(.5);
obj.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),dir.normalize());
beamGroup.add(obj);
}

addBeam([-1.35,.55,-.65],[-.95,.55,-.65],'#f59e0b');
addBeam([-.35,.55,-.65],[.2,2.2,-.15],'#22d3ee');
addBeam([.5,2.2,-.15],[1.35,.55,-.65],'#22d3ee');
beamGroup.visible=false;

function updateCamera(){
phi=Math.max(.25,Math.min(1.5,phi));
radius=Math.max(5,Math.min(16,radius));
camera.position.set(
radius*Math.sin(phi)*Math.sin(theta),
radius*Math.cos(phi)+1.2,
radius*Math.sin(phi)*Math.cos(theta)
);
camera.lookAt(0,1,0);
}
updateCamera();

let dragging=false,lastX=0,lastY=0,downX=0,downY=0;
const raycaster=new THREE.Raycaster();
const pointer=new THREE.Vector2();

renderer.domElement.addEventListener('pointerdown',e=>{
dragging=true;
lastX=downX=e.clientX;
lastY=downY=e.clientY;
renderer.domElement.setPointerCapture(e.pointerId);
});

renderer.domElement.addEventListener('pointermove',e=>{
if(!dragging)return;
theta-=(e.clientX-lastX)*.008;
phi+=(e.clientY-lastY)*.008;
lastX=e.clientX;
lastY=e.clientY;
updateCamera();
});

renderer.domElement.addEventListener('pointerup',e=>{
dragging=false;
if(Math.abs(e.clientX-downX)+Math.abs(e.clientY-downY)>6)return;
const rect=renderer.domElement.getBoundingClientRect();
pointer.x=((e.clientX-rect.left)/rect.width)*2-1;
pointer.y=-((e.clientY-rect.top)/rect.height)*2+1;
raycaster.setFromCamera(pointer,camera);
const hit=raycaster.intersectObjects(clickable,false)[0];
if(hit){
document.getElementById('partTitle').textContent=hit.object.userData.name;
document.getElementById('partInfo').textContent=hit.object.userData.description;
}
});

renderer.domElement.addEventListener('wheel',e=>{
e.preventDefault();
radius+=e.deltaY*.008;
updateCamera();
},{passive:false});

window.toggleRotation=function(){
auto=!auto;
document.getElementById('rotationButton').textContent=
auto?'Ⅱ Hentikan putaran':'⟳ Putar otomatis';
};

window.toggleLid=function(){
lidOpen=!lidOpen;
lid.rotation.x=lidOpen?-1.05:0;
};

window.toggleBeam=function(){
beamOn=!beamOn;
beamGroup.visible=beamOn;
document.getElementById('beamButton').textContent=
beamOn?'Jalur cahaya: aktif':'Jalur cahaya';
};

window.resetModel=function(){
theta=.7;phi=1;radius=9;
auto=false;lidOpen=false;beamOn=false;
lid.rotation.x=0;
beamGroup.visible=false;
updateCamera();
document.getElementById('rotationButton').textContent='⟳ Putar otomatis';
document.getElementById('beamButton').textContent='Jalur cahaya';
document.getElementById('partTitle').textContent='Pilih komponen';
document.getElementById('partInfo').textContent='Seret model untuk memutar dan klik komponen untuk melihat fungsinya.';
};

function animate(){
requestAnimationFrame(animate);
if(auto&&!dragging){theta+=.005;updateCamera();}
renderer.render(scene,camera);
}
animate();

window.addEventListener('resize',()=>{
camera.aspect=root.clientWidth/root.clientHeight;
camera.updateProjectionMatrix();
renderer.setSize(root.clientWidth,root.clientHeight);
});
})();
</script>
"""


# =========================
# NAVIGASI
# =========================
if "halaman" not in st.session_state:
    st.session_state.halaman = "Home"

st.markdown("""
<div style="display:flex;align-items:center;gap:10px">
<h2 style="color:#0a1f44;margin:0">🔬 UV-Vis <span style="color:#0891b2">Explorer</span></h2>
</div>
""", unsafe_allow_html=True)

menu = st.columns(4)
for col, nama in zip(menu, ["Home", "Teori", "Model 3D", "Perhitungan"]):
    if col.button(nama, use_container_width=True):
        st.session_state.halaman = nama

halaman = st.session_state.halaman
st.divider()


# =========================
# HOME
# =========================
if halaman == "Home":

    st.markdown("""
    <div class="hero">
    <h1>Jelajahi Dunia Spektrofotometri UV-Vis</h1>
    <p>Laboratorium virtual untuk memahami prinsip spektrofotometri,
    mengenal komponen instrumen melalui model 3D, dan berlatih
    perhitungan analisis kuantitatif.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Menu Utama</div>', unsafe_allow_html=True)

    c1,c2,c3=st.columns(3)

    with c1:
        st.markdown("""
        <div class="card">
        <h2>📘 Teori</h2>
        Pelajari prinsip absorpsi cahaya, komponen alat, dan Hukum Lambert-Beer.
        </div>
        """,unsafe_allow_html=True)
        if st.button("Pelajari Teori →",use_container_width=True):
            st.session_state.halaman="Teori"
            st.rerun()

    with c2:
        st.markdown("""
        <div class="card">
        <h2>🧊 Model 3D</h2>
        Jelajahi bagian spektrofotometer melalui model interaktif.
        </div>
        """,unsafe_allow_html=True)
        if st.button("Buka Model 3D →",use_container_width=True):
            st.session_state.halaman="Model 3D"
            st.rerun()

    with c3:
        st.markdown("""
        <div class="card">
        <h2>🧮 Perhitungan</h2>
        Hitung absorbansi, transmitansi, konsentrasi, dan kurva kalibrasi.
        </div>
        """,unsafe_allow_html=True)
        if st.button("Mulai Perhitungan →",use_container_width=True):
            st.session_state.halaman="Perhitungan"
            st.rerun()

    st.info("Aplikasi ini merupakan media pembelajaran. Gunakan data hasil praktikum untuk analisis nyata.")


# =========================
# TEORI
# =========================
elif halaman == "Teori":

    st.markdown('<div class="section-title">Pengertian Spektrofotometri UV-Vis</div>',unsafe_allow_html=True)

    st.write("""
    Spektrofotometri UV-Vis merupakan metode analisis instrumental yang
    mengukur penyerapan radiasi ultraviolet dan cahaya tampak oleh suatu
    zat. Metode ini dapat digunakan untuk menentukan konsentrasi analit
    berdasarkan hubungan antara absorbansi dan konsentrasi.
    """)

    st.markdown('<div class="section-title">Prinsip Dasar</div>',unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <h3>⚛️ Absorpsi cahaya</h3>
    Molekul menyerap energi foton ketika energi radiasi sesuai dengan
    perbedaan tingkat energi elektronik molekul. Penyerapan ini menghasilkan
    spektrum yang dapat menjadi karakteristik suatu senyawa.
    </div>
    <div class="card">
    <h3>🌈 Panjang gelombang</h3>
    Spektrofotometer memilih panjang gelombang tertentu menggunakan
    monokromator. Pengukuran sering dilakukan pada panjang gelombang
    maksimum (λmaks) untuk memperoleh sensitivitas yang baik.
    </div>
    <div class="card">
    <h3>🧪 Kuvet</h3>
    Kuvet digunakan sebagai wadah sampel. Kuvet kuarsa cocok untuk pengukuran
    UV, sedangkan kuvet kaca umumnya digunakan pada daerah cahaya tampak.
    </div>
    """,unsafe_allow_html=True)

    st.markdown('<div class="section-title">Komponen Instrumen</div>',unsafe_allow_html=True)

    komponen = {
        "Sumber cahaya":"Menghasilkan radiasi UV dan cahaya tampak.",
        "Monokromator":"Memisahkan cahaya dan memilih panjang gelombang tertentu.",
        "Celah optik":"Mengatur lebar berkas cahaya yang melewati sistem optik.",
        "Kuvet":"Menampung larutan sampel pada lintasan cahaya.",
        "Detektor":"Mengubah intensitas cahaya menjadi sinyal listrik.",
        "Pengolah sinyal":"Menghitung dan mengolah sinyal pengukuran.",
        "Layar":"Menampilkan nilai absorbansi, transmitansi, atau spektrum."
    }

    for nama,fungsi in komponen.items():
        with st.expander(nama):
            st.write(fungsi)

    st.markdown('<div class="section-title">Hukum Lambert-Beer</div>',unsafe_allow_html=True)

    st.latex(r"A=\varepsilon b c")
    st.write("""
    Keterangan:
    - A = absorbansi
    - ε = absorptivitas molar (L mol⁻¹ cm⁻¹)
    - b = panjang lintasan optik (cm)
    - c = konsentrasi (mol/L)
    """)

    st.latex(r"A=-\log_{10}(T)")
    st.latex(r"T=\frac{I}{I_0}")
    st.latex(r"\%T=100T")

    st.markdown("""
    <div class="note">
    Dalam rentang linear, absorbansi berbanding lurus dengan konsentrasi
    analit dan panjang lintasan optik.
    </div>
    """,unsafe_allow_html=True)

    st.markdown('<div class="section-title">Alur Kerja</div>',unsafe_allow_html=True)
    st.write("""
    Sumber cahaya → Monokromator → Kuvet berisi sampel → Detektor →
    Pengolah sinyal → Hasil pengukuran.
    """)

    st.markdown('<div class="section-title">Faktor yang Memengaruhi Hasil</div>',unsafe_allow_html=True)

    faktor = [
        "Konsentrasi sampel terlalu tinggi.",
        "Panjang gelombang pengukuran tidak sesuai.",
        "Kuvet kotor, tergores, atau terdapat gelembung.",
        "Sampel keruh sehingga terjadi hamburan cahaya.",
        "Perubahan pH, suhu, atau kondisi kimia sampel.",
        "Cahaya liar dan kondisi instrumen."
    ]

    for f in faktor:
        st.markdown(f"- {f}")


# =========================
# MODEL 3D
# =========================
elif halaman == "Model 3D":

    st.markdown('<div class="section-title">Model 3D Spektrofotometer UV-Vis</div>',unsafe_allow_html=True)

    st.markdown("""
    <div class="note">
    🖱️ Seret model untuk memutar. Gunakan scroll untuk zoom.
    Klik komponen untuk membaca fungsinya, dan gunakan tombol untuk
    menampilkan jalur cahaya atau membuka tutup kompartemen.
    </div>
    """,unsafe_allow_html=True)

    components.html(MODEL_3D,height=600,scrolling=False)

    st.caption("Model 3D ini merupakan ilustrasi edukasi, bukan replika instrumen dari merek tertentu.")


# =========================
# PERHITUNGAN
# =========================
elif halaman == "Perhitungan":

    st.markdown('<div class="section-title">Kalkulator Spektrofotometri</div>',unsafe_allow_html=True)

    tab1,tab2,tab3=st.tabs([
        "Absorbansi & Transmitansi",
        "Lambert-Beer",
        "Kurva Kalibrasi"
    ])

    # -------------------------
    # ABSORBANSI & TRANSMITANSI
    # -------------------------
    with tab1:
        st.subheader("Konversi Absorbansi dan Transmitansi")

        pilihan=st.radio(
            "Pilih data yang diketahui",
            ["Transmitansi (T)","Persen transmitansi (%T)","Absorbansi (A)"],
            horizontal=True
        )

        nilai=st.number_input("Masukkan nilai",value=0.5,step=0.01,format="%.5f")

        if st.button("Hitung",key="hitung_at"):
            try:
                if pilihan=="Transmitansi (T)":
                    T=nilai
                    A=hitung_absorbansi(T)

                elif pilihan=="Persen transmitansi (%T)":
                    if nilai<=0 or nilai>100:
                        raise ValueError("%T harus lebih dari 0 sampai 100.")
                    T=nilai/100
                    A=hitung_absorbansi(T)

                else:
                    A=nilai
                    T=hitung_transmitansi(A)

                c1,c2,c3=st.columns(3)
                c1.metric("Absorbansi",f"{A:.5f}")
                c2.metric("Transmitansi",f"{T:.6f}")
                c3.metric("Transmitansi (%)",f"{T*100:.3f}%")

                st.latex(r"A=-\log_{10}(T)")
                st.write(f"A = −log₁₀({T:.6f}) = {A:.5f}")

            except ValueError as e:
                st.error(str(e))

    # -------------------------
    # LAMBERT-BEER
    # -------------------------
    with tab2:
        st.subheader("Menghitung Konsentrasi")

        st.latex(r"c=\frac{A}{\varepsilon b}")

        col1,col2,col3=st.columns(3)

        with col1:
            A=st.number_input("Absorbansi (A)",min_value=0.0,value=0.450,step=0.01)

        with col2:
            epsilon=st.number_input("ε (L mol⁻¹ cm⁻¹)",min_value=0.000001,value=12000.0,step=100.0)

        with col3:
            b=st.number_input("Panjang lintasan (cm)",min_value=0.000001,value=1.0,step=0.1)

        if st.button("Hitung Konsentrasi"):
            try:
                c=hitung_konsentrasi(A,epsilon,b)

                st.success(f"Konsentrasi = {c:.5e} mol/L")
                st.write(f"Konsentrasi = {c*1000:.5f} mmol/L")
                st.write("Langkah perhitungan:")
                st.write(f"c = A / (ε × b)")
                st.write(f"c = {A} / ({epsilon} × {b})")
                st.write(f"c = {c:.5e} mol/L")

            except ValueError as e:
                st.error(str(e))

    # -------------------------
    # KURVA KALIBRASI
    # -------------------------
    with tab3:
        st.subheader("Kurva Kalibrasi")

        st.info("Data berikut adalah data simulasi untuk latihan. Ganti dengan data hasil praktikum.")

        data_awal=pd.DataFrame({
            "Konsentrasi (mg/L)":[0,2,4,6,8,10],
            "Absorbansi":[0.002,0.101,0.205,0.298,0.405,0.502]
        })

        data=st.data_editor(
            data_awal,
            num_rows="dynamic",
            use_container_width=True,
            key="tabel_kalibrasi"
        )

        A_sampel=st.number_input("Absorbansi sampel",value=0.350,step=0.01)

        if st.button("Buat Kurva Kalibrasi"):
            try:
                d=data.apply(pd.to_numeric,errors="coerce").dropna()

                if len(d)<3:
                    raise ValueError("Masukkan minimal 3 baris data yang lengkap.")

                x=d.iloc[:,0].to_numpy(dtype=float)
                y=d.iloc[:,1].to_numpy(dtype=float)

                if np.any(x<0):
                    raise ValueError("Konsentrasi tidak boleh negatif.")

                if len(np.unique(x))<2:
                    raise ValueError("Gunakan konsentrasi yang berbeda.")

                m,b0=np.polyfit(x,y,1)
                pred=m*x+b0

                ss_res=np.sum((y-pred)**2)
                ss_tot=np.sum((y-np.mean(y))**2)
                r2=1-ss_res/ss_tot if ss_tot!=0 else 1.0

                c1,c2=st.columns(2)
                c1.metric("Persamaan regresi",f"y = {m:.5f}x + {b0:.5f}")
                c2.metric("Koefisien determinasi R²",f"{r2:.5f}")

                if abs(m)<1e-12:
                    raise ValueError("Kemiringan garis terlalu kecil untuk menghitung konsentrasi.")

                konsentrasi=(A_sampel-b0)/m

                st.success(f"Perkiraan konsentrasi sampel = {konsentrasi:.4f} mg/L")

                xx=np.linspace(min(x),max(x),100)
                fig=go.Figure()

                fig.add_trace(go.Scatter(
                    x=x,y=y,mode="markers",name="Data standar",
                    marker=dict(size=10)
                ))

                fig.add_trace(go.Scatter(
                    x=xx,y=m*xx+b0,mode="lines",name="Regresi linear"
                ))

                fig.add_trace(go.Scatter(
                    x=[konsentrasi],y=[A_sampel],
                    mode="markers",name="Sampel",
                    marker=dict(size=13,symbol="star")
                ))

                fig.update_layout(
                    template="plotly_white",
                    xaxis_title="Konsentrasi (mg/L)",
                    yaxis_title="Absorbansi",
                    height=450
                )

                st.plotly_chart(fig,use_container_width=True)

                if r2<0.99:
                    st.warning("R² kurang dari 0,99. Periksa kembali data dan linearitas kurva.")

                if konsentrasi<min(x) or konsentrasi>max(x):
                    st.warning("Konsentrasi sampel berada di luar rentang standar. Hasil merupakan ekstrapolasi.")

            except (ValueError,TypeError) as e:
                st.error(str(e))


# =========================
# FOOTER
# =========================
st.divider()
st.markdown("""
<div style="text-align:center;color:#64748b;padding:10px">
🔬 <b>UV-Vis Explorer</b><br>
Laboratorium Virtual Spektrofotometri UV-Vis<br>
Media pembelajaran dan simulasi analisis instrumental
</div>
""",unsafe_allow_html=True)
