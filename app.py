import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

import calc
from viewer import VIEWER_HTML

st.set_page_config(page_title="UV-Vis Explorer", page_icon="🔬", layout="wide",
                   initial_sidebar_state="collapsed")

PAGES = ["Home", "Teori", "Model 3D", "Perhitungan"]
ICONS = {"Home": "🏠", "Teori": "📘", "Model 3D": "🧊", "Perhitungan": "🧮"}
DEFAULT_CAL = pd.DataFrame({
    "Konsentrasi (mg/L)": [0.0, 2.0, 4.0, 6.0, 8.0, 10.0],
    "Absorbansi": [0.002, 0.101, 0.205, 0.298, 0.405, 0.502],
})

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif}
.stApp{background:linear-gradient(180deg,#f4f7fb 0%,#eaf1f9 100%)}
header[data-testid="stHeader"],#MainMenu,footer{visibility:hidden;height:0}
.block-container{padding-top:1.2rem;max-width:1180px}
.logo{font-weight:800;font-size:1.5rem;color:#0a1f44;letter-spacing:-.5px}
.logo span{color:#06b6d4}
.hero{background:linear-gradient(135deg,#0a1f44 0%,#12366b 60%,#0e7490 100%);border-radius:24px;padding:2.5rem;color:#fff;
box-shadow:0 20px 50px rgba(10,31,68,.25);animation:fade .8s ease both}
.hero h1{font-size:2.5rem;font-weight:800;line-height:1.15;margin:.2rem 0 1rem;color:#fff}
.hero p{color:#cfe3f5;font-size:1.05rem;line-height:1.6}
.badge{display:inline-block;background:rgba(6,182,212,.2);color:#67e8f9;border:1px solid rgba(103,232,249,.4);border-radius:999px;padding:4px 14px;font-size:.8rem}
.card{background:#fff;border-radius:18px;padding:1.3rem 1.4rem;box-shadow:0 6px 24px rgba(10,31,68,.08);border:1px solid #e2e8f0;
height:100%;transition:transform .25s,box-shadow .25s;animation:fade .8s ease both}
.card:hover{transform:translateY(-4px);box-shadow:0 14px 32px rgba(6,182,212,.2)}
.card .ic{font-size:2rem}.card h4{margin:.4rem 0;color:#0a1f44}.card p{color:#475569;font-size:.93rem;margin:0;line-height:1.55}
.sec{color:#0a1f44;font-weight:800;font-size:1.5rem;margin:1.6rem 0 .6rem;border-left:5px solid #06b6d4;padding-left:.7rem}
.flow{display:flex;flex-wrap:wrap;gap:.4rem;align-items:center;margin:.5rem 0}
.step{background:#0a1f44;color:#fff;border-radius:12px;padding:.6rem .9rem;font-size:.85rem;font-weight:600}
.arrow{color:#06b6d4;font-weight:800;font-size:1.2rem}
.spec{height:34px;border-radius:10px;background:linear-gradient(90deg,#4b0082 0%,#4b0082 6%,#6a0dad 12%,#2563eb 22%,#06b6d4 32%,#22c55e 45%,#eab308 60%,#f97316 75%,#dc2626 90%,#7f1d1d 100%)}
.note{background:#ecfeff;border:1px solid #a5f3fc;border-radius:12px;padding:.8rem 1rem;color:#0e5566;font-size:.9rem}
.stButton>button{border-radius:12px;font-weight:600;border:1px solid #cbd5e1;transition:all .2s}
.stButton>button:hover{border-color:#06b6d4;color:#0891b2;transform:translateY(-1px)}
.stButton>button[kind="primary"]{background:linear-gradient(90deg,#0a1f44,#0e7490);color:#fff;border:none}
.foot{text-align:center;color:#64748b;font-size:.85rem;margin:2.5rem 0 .5rem;padding-top:1rem;border-top:1px solid #dbe4ef}
@keyframes fade{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
@media(max-width:768px){.hero{padding:1.4rem}.hero h1{font-size:1.7rem}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ---------------- state ----------------
def init_state():
    d = {"page": "Home", "t1_mode": "Transmitansi (fraksi)", "t1_T": 0.5, "t1_P": 50.0, "t1_A": 0.301,
         "t2_eps": 12000.0, "t2_b": 1.0, "t2_A": 0.450, "cal_A": 0.350}
    for k, v in d.items():
        st.session_state.setdefault(k, v)
    st.session_state.setdefault("cal_df", DEFAULT_CAL.copy())

def go_page(p):
    st.session_state.page = p

def reset_t1():
    st.session_state.update(t1_mode="Transmitansi (fraksi)", t1_T=0.5, t1_P=50.0, t1_A=0.301)

def reset_t2():
    st.session_state.update(t2_eps=12000.0, t2_b=1.0, t2_A=0.450)

def reset_t3():
    st.session_state.cal_df = DEFAULT_CAL.copy()
    st.session_state.pop("cal_editor", None)
    st.session_state.cal_A = 0.350

init_state()

def card(icon, title, body):
    return f'<div class="card"><div class="ic">{icon}</div><h4>{title}</h4><p>{body}</p></div>'

def nav():
    cols = st.columns([2.2, 1, 1, 1, 1.2])
    cols[0].markdown('<div class="logo">🔬 UV-Vis <span>Explorer</span></div>', unsafe_allow_html=True)
    for c, p in zip(cols[1:], PAGES):
        c.button(f"{ICONS[p]} {p}", key=f"nav_{p}", on_click=go_page, args=(p,), use_container_width=True,
                 type="primary" if st.session_state.page == p else "secondary")

def back_home():
    st.button("← Kembali ke Home", key=f"back_{st.session_state.page}", on_click=go_page, args=("Home",))

HERO_SVG = """
<svg viewBox="0 0 420 260" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:440px">
<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#e2e8f0"/><stop offset="1" stop-color="#94a3b8"/></linearGradient>
<linearGradient id="b" x1="0" x2="1"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#67e8f9"/></linearGradient></defs>
<ellipse cx="210" cy="232" rx="170" ry="14" fill="rgba(0,0,0,.25)"/>
<rect x="30" y="100" width="360" height="120" rx="16" fill="url(#g)"/>
<rect x="30" y="100" width="360" height="22" rx="10" fill="#cbd5e1"/>
<rect x="50" y="140" width="110" height="56" rx="8" fill="#052b3a"/>
<text x="60" y="164" fill="#22d3ee" font-family="monospace" font-size="14">A = 0.452</text>
<text x="60" y="184" fill="#22d3ee" font-family="monospace" font-size="11">λ = 540 nm</text>
<rect x="250" y="130" width="120" height="70" rx="8" fill="#24324d"/>
<circle cx="275" cy="155" r="8" fill="#06b6d4"/><circle cx="305" cy="155" r="8" fill="#cbd5e1"/><circle cx="335" cy="155" r="8" fill="#cbd5e1"/>
<rect x="190" y="70" width="70" height="38" rx="6" fill="#1d3557"/><rect x="208" y="52" width="34" height="22" rx="4" fill="#0e7490"/>
<rect x="212" y="40" width="26" height="16" rx="3" fill="#a5f3fc" opacity=".8"/>
<rect x="0" y="108" width="40" height="8" fill="url(#b)" opacity=".9"><animate attributeName="opacity" values=".3;1;.3" dur="2s" repeatCount="indefinite"/></rect>
</svg>"""

# ---------------- HOME ----------------
def page_home():
    c1, c2 = st.columns([1.15, 1], gap="large")
    with c1:
        st.markdown("""<div class="hero"><span class="badge">🧪 Laboratorium Virtual • Aplikasi Edukasi</span>
<h1>Jelajahi Dunia Spektrofotometri UV-Vis</h1>
<p>UV-Vis Explorer membantu mahasiswa memahami teori absorpsi cahaya, mengenal komponen instrumen lewat model 3D interaktif,
dan berlatih menghitung absorbansi, transmitansi, konsentrasi, serta kurva kalibrasi.</p></div>""", unsafe_allow_html=True)
        st.write("")
        st.button("🚀 Mulai Eksplorasi", key="cta", type="primary", on_click=go_page, args=("Teori",))
    with c2:
        st.markdown(f'<div style="display:flex;justify-content:center;padding:1rem">{HERO_SVG}</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec">Menu Utama</div>', unsafe_allow_html=True)
    items = [("Teori", "📘", "Konsep dasar, komponen alat, alur kerja, dan Hukum Lambert-Beer secara terstruktur."),
             ("Model 3D", "🧊", "Putar, zoom, dan klik komponen spektrofotometer; lihat animasi jalur cahaya."),
             ("Perhitungan", "🧮", "Kalkulator A–T, konsentrasi Lambert-Beer, dan kurva kalibrasi dengan regresi.")]
    for col, (p, ic, d) in zip(st.columns(3, gap="large"), items):
        with col:
            st.markdown(card(ic, p, d), unsafe_allow_html=True)
            st.button(f"Buka {p} →", key=f"card_{p}", on_click=go_page, args=(p,), use_container_width=True)

# ---------------- TEORI ----------------
def page_teori():
    back_home()
    st.markdown('<div class="sec">1. Pengertian Spektrofotometri UV-Vis</div>', unsafe_allow_html=True)
    st.write("Spektrofotometri UV-Vis adalah teknik analisis kuantitatif yang mengukur seberapa besar radiasi ultraviolet dan "
             "cahaya tampak diserap (absorbansi) atau diteruskan (transmitansi) oleh suatu larutan pada panjang gelombang tertentu. "
             "Hasilnya dipakai untuk menentukan konsentrasi analit yang menyerap radiasi.")
    st.markdown('<div class="sec">2. Prinsip Dasar Absorpsi Radiasi</div>', unsafe_allow_html=True)
    a, b = st.columns(2)
    a.markdown(card("⚛️", "Transisi elektronik", "Molekul menyerap foton jika energinya (E = hc/λ) sama dengan selisih energi antara orbital "
        "keadaan dasar dan tereksitasi, misalnya transisi π→π* dan n→π*. Ini sebabnya tiap zat punya spektrum khas."), unsafe_allow_html=True)
    b.markdown(card("🎨", "Warna larutan", "Larutan tampak berwarna karena menyerap sebagian panjang gelombang tampak; warna yang terlihat adalah "
        "warna komplementer dari cahaya yang diserap."), unsafe_allow_html=True)
    st.markdown('<div class="sec">3. Rentang Ultraviolet dan Cahaya Tampak</div>', unsafe_allow_html=True)
    st.markdown('<div class="spec"></div><div style="display:flex;justify-content:space-between;font-size:.8rem;color:#475569;margin-top:4px">'
                '<span>190 nm</span><span>UV dekat 190–400 nm</span><span>Tampak 400–780 nm</span><span>1100 nm</span></div>', unsafe_allow_html=True)
    st.caption("Warna pada bar hanya ilustrasi. Instrumen UV-Vis umumnya bekerja pada ±190–1100 nm; UV di bawah 190 nm diserap oksigen udara.")
    st.markdown('<div class="sec">4. Fungsi Komponen Alat</div>', unsafe_allow_html=True)
    comps = [("💡", "Sumber cahaya", "Lampu deuterium (UV) dan tungsten/halogen (tampak) menghasilkan radiasi kontinu."),
             ("🌈", "Monokromator", "Kisi difraksi/prisma memisahkan panjang gelombang dan memilih satu pita sempit."),
             ("↔️", "Celah optik", "Mengatur lebar berkas dan lebar pita spektral; memengaruhi resolusi dan intensitas."),
             ("🧪", "Kuvet", "Wadah sampel dengan lintasan b (biasanya 1 cm). Kuarsa untuk UV, kaca/plastik untuk tampak."),
             ("📡", "Detektor", "Fotodioda atau PMT mengubah intensitas cahaya menjadi sinyal listrik."),
             ("🔌", "Pengolah sinyal", "Menguatkan sinyal, mengubahnya digital, dan menghitung T serta A terhadap blanko."),
             ("🖥️", "Layar & sistem kontrol", "Menampilkan hasil dan mengatur λ, blanko, serta mode pengukuran.")]
    for i in range(0, len(comps), 3):
        for col, (ic, t, d) in zip(st.columns(3), comps[i:i + 3]):
            col.markdown(card(ic, t, d), unsafe_allow_html=True)
        st.write("")
    st.markdown('<div class="sec">5. Alur Kerja Instrumen</div>', unsafe_allow_html=True)
    steps = ["Sumber cahaya", "Monokromator", "Celah", "Kuvet + sampel", "Detektor", "Pengolah sinyal", "Layar (A, %T)"]
    st.markdown('<div class="flow">' + '<span class="arrow">➜</span>'.join(f'<span class="step">{s}</span>' for s in steps) + '</div>',
                unsafe_allow_html=True)
    st.write("Cahaya polikromatik dari sumber diuraikan menjadi cahaya hampir monokromatik, dilewatkan melalui kuvet berisi sampel, "
             "lalu intensitas yang diteruskan (I) dibandingkan dengan intensitas blanko (I₀) untuk memperoleh T dan A.")
    st.markdown('<div class="sec">6. Blanko, λmaks, Absorbansi, dan Transmitansi</div>', unsafe_allow_html=True)
    x, y = st.columns(2)
    x.markdown(card("⬜", "Blanko", "Larutan tanpa analit (pelarut dan reagen yang sama) untuk mengatur A = 0 sehingga serapan pelarut dan kuvet tidak ikut terhitung."), unsafe_allow_html=True)
    y.markdown(card("📈", "λmaks", "Panjang gelombang dengan serapan tertinggi. Pengukuran dilakukan di λmaks karena sensitivitas paling besar dan kesalahan akibat pergeseran λ paling kecil."), unsafe_allow_html=True)
    st.write("")
    x, y = st.columns(2)
    x.markdown(card("🔦", "Transmitansi (T)", "Fraksi cahaya yang diteruskan: T = I/I₀. Dalam persen: %T = 100 × T."), unsafe_allow_html=True)
    y.markdown(card("🌑", "Absorbansi (A)", "Ukuran banyaknya cahaya yang diserap: A = −log₁₀(T). Tidak memiliki satuan."), unsafe_allow_html=True)
    st.markdown('<div class="sec">7. Hukum Lambert-Beer</div>', unsafe_allow_html=True)
    st.latex(r"A = \varepsilon\, b\, c \qquad A = -\log_{10}(T) \qquad \%T = 100 \times T")
    st.markdown("""
- **A** = absorbansi (tanpa satuan)
- **ε** = absorptivitas molar (L mol⁻¹ cm⁻¹)
- **b** = panjang lintasan optik (cm)
- **c** = konsentrasi (mol/L)
- **T** = transmitansi dalam bentuk fraksi (0–1)
""")
    st.markdown('<div class="note">Absorbansi berbanding lurus dengan konsentrasi dan panjang lintasan. Contoh: T = 0,10 → A = 1; T = 0,01 → A = 2.</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec">8. Faktor yang Memengaruhi dan Keterbatasan</div>', unsafe_allow_html=True)
    for t, d in [("Konsentrasi tinggi", "Pada larutan pekat, interaksi antarmolekul menyebabkan penyimpangan linearitas dari Hukum Lambert-Beer."),
                 ("Cahaya tidak monokromatik & stray light", "Menyebabkan kurva kalibrasi melengkung, terutama pada A tinggi (>1,5)."),
                 ("Kondisi kimia", "pH, suhu, kesetimbangan kimia, dan reaksi samping dapat mengubah spesies penyerap dan nilai ε."),
                 ("Hamburan & sampel keruh", "Partikel menghamburkan cahaya sehingga terbaca sebagai absorbansi palsu."),
                 ("Kuvet & penanganan", "Sidik jari, goresan, gelembung, dan bahan kuvet yang tidak sesuai UV memengaruhi hasil."),
                 ("Rentang optimum", "Akurasi terbaik umumnya pada A ≈ 0,2–0,8 (atau 0,1–1,0). Zat harus memiliki kromofor atau diubah menjadi senyawa berwarna.")]:
        with st.expander(t):
            st.write(d)

# ---------------- 3D ----------------
def page_3d():
    back_home()
    st.markdown('<div class="sec">Model 3D Spektrofotometer UV-Vis</div>', unsafe_allow_html=True)
    st.markdown('<div class="note">🖱️ Seret untuk memutar 360° • Scroll untuk zoom • Klik komponen untuk melihat informasi • '
                'Gunakan tombol untuk membuka kuvet dan melihat jalur cahaya. Model dibuat dari bentuk dasar sebagai '
                '<b>visualisasi edukasi</b>, bukan gambar pasti satu merek instrumen komersial.</div>', unsafe_allow_html=True)
    st.write("")
    components.html(VIEWER_HTML, height=650, scrolling=False)
    st.caption("Jika model tidak muncul, pastikan browser mendukung WebGL dan koneksi internet dapat mengakses cdnjs.cloudflare.com.")

# ---------------- PERHITUNGAN ----------------
def fmt(x, d=4):
    return f"{x:.{d}f}"

def tab_at():
    st.subheader("Absorbansi ↔ Transmitansi")
    st.latex(r"A=-\log_{10}(T)\quad;\quad T=10^{-A}\quad;\quad \%T=100\,T")
    modes = {"Transmitansi (fraksi)": ("T", "t1_T", "Nilai T (0 < T ≤ 1)"), "Persen transmitansi (%T)": ("P", "t1_P", "Nilai %T (0 < %T ≤ 100)"),
             "Absorbansi (A)": ("A", "t1_A", "Nilai A (≥ 0)")}
    st.radio("Data yang diketahui", list(modes), key="t1_mode", horizontal=True)
    mode, key, label = modes[st.session_state.t1_mode]
    st.number_input(label, key=key, format="%.6f", step=0.01)
    try:
        r = calc.convert(mode, st.session_state[key])
        c1, c2, c3 = st.columns(3)
        c1.metric("Absorbansi (A)", fmt(r["A"]))
        c2.metric("Transmitansi (T)", fmt(r["T"], 5))
        c3.metric("% Transmitansi", fmt(r["P"], 3) + " %")
        st.info(f"A = −log₁₀({r['T']:.5f}) = {r['A']:.4f}  |  T = 10^(−{r['A']:.4f}) = {r['T']:.5f}  |  %T = 100 × {r['T']:.5f} = {r['P']:.3f}%")
        if r["A"] > 2:
            st.warning("A > 2: hanya <1% cahaya diteruskan; pembacaan kurang andal. Encerkan sampel.")
    except ValueError as e:
        st.error(str(e))
    st.button("↺ Reset tab ini", key="rst1", on_click=reset_t1)

def tab_lb():
    st.subheader("Konsentrasi dari Hukum Lambert-Beer")
    st.latex(r"c=\dfrac{A}{\varepsilon\, b}")
    c1, c2, c3 = st.columns(3)
    c1.number_input("ε (L mol⁻¹ cm⁻¹)", key="t2_eps", format="%.2f", step=100.0)
    c2.number_input("b (cm)", key="t2_b", format="%.3f", step=0.1)
    c3.number_input("Absorbansi A", key="t2_A", format="%.4f", step=0.01)
    A, eps, b = st.session_state.t2_A, st.session_state.t2_eps, st.session_state.t2_b
    try:
        c = calc.concentration(A, eps, b)
        st.success(f"Konsentrasi c = {c:.4e} mol/L  ({c*1e3:.4f} mmol/L = {c*1e6:.2f} µmol/L)")
        st.markdown(f"**Langkah perhitungan**\n\n1. Rumus: c = A / (ε · b)\n\n2. Substitusi: c = {A:g} / ({eps:g} × {b:g})\n\n"
                    f"3. Penyebut: ε · b = {eps*b:g} L mol⁻¹\n\n4. Hasil: c = {c:.4e} mol/L")
        if A > 1.5:
            st.warning("A tinggi (>1,5): kemungkinan keluar dari rentang linear. Encerkan sampel.")
        elif A < 0.1:
            st.warning("A sangat rendah (<0,1): ketidakpastian relatif besar.")
    except ValueError as e:
        st.error(str(e))
    st.caption("Nilai awal (ε = 12000, b = 1 cm, A = 0,450) adalah contoh simulasi untuk latihan.")
    st.button("↺ Reset tab ini", key="rst2", on_click=reset_t2)

def tab_cal():
    st.subheader("Kurva Kalibrasi")
    st.markdown('<div class="note">⚠️ Data awal di bawah adalah <b>data simulasi</b> untuk latihan, bukan hasil pengukuran laboratorium nyata. '
                'Edit nilai atau tambah baris sesuai data Anda.</div>', unsafe_allow_html=True)
    edited = st.data_editor(st.session_state.cal_df, num_rows="dynamic", key="cal_editor", use_container_width=True,
                            column_config={c: st.column_config.NumberColumn(format="%.4f") for c in DEFAULT_CAL.columns})
    st.session_state.cal_df = pd.DataFrame(edited)
    st.number_input("Absorbansi sampel", key="cal_A", format="%.4f", step=0.01)
    try:
        x, y = calc.clean_calibration(edited)
        reg = calc.linear_regression(x, y)
        m, b, r2 = reg["m"], reg["b"], reg["r2"]
        c1, c2, c3 = st.columns(3)
        c1.metric("Persamaan", f"y = {m:.4f}x {'+' if b >= 0 else '−'} {abs(b):.4f}")
        c2.metric("R²", f"{r2:.5f}")
        c3.metric("Jumlah titik", reg["n"])
        if r2 < 0.99:
            st.warning("R² < 0,99: linearitas kurang baik. Periksa data atau rentang konsentrasi.")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode="markers", name="Data standar", marker=dict(size=11, color="#0a1f44")))
        xl = np.linspace(x.min(), x.max(), 50)
        fig.add_trace(go.Scatter(x=xl, y=m * xl + b, mode="lines", name="Regresi linear", line=dict(color="#06b6d4", width=3)))
        try:
            As = st.session_state.cal_A
            xs = calc.predict_concentration(As, m, b)
            fig.add_trace(go.Scatter(x=[xs], y=[As], mode="markers", name="Sampel",
                                     marker=dict(size=15, color="#f97316", symbol="star")))
            st.success(f"Konsentrasi sampel ≈ {xs:.4f} (satuan sama dengan kolom konsentrasi) — x = (A − b)/m = ({As:g} − {b:.4f}) / {m:.4f}")
            if xs < 0:
                st.warning("Hasil negatif: absorbansi sampel lebih kecil dari intersep kurva.")
            elif xs < x.min() or xs > x.max() or As < y.min() or As > y.max():
                st.warning("Sampel berada di luar rentang kalibrasi (ekstrapolasi); hasil kurang andal.")
        except ValueError as e:
            st.error(str(e))
        fig.update_layout(template="plotly_white", height=430, xaxis_title="Konsentrasi", yaxis_title="Absorbansi (A)",
                          legend=dict(orientation="h", y=1.12), margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig, use_container_width=True)
    except ValueError as e:
        st.error(str(e))
    st.button("↺ Reset data kalibrasi", key="rst3", on_click=reset_t3)

def page_calc():
    back_home()
    st.markdown('<div class="sec">Kalkulator Spektrofotometri</div>', unsafe_allow_html=True)
    t1, t2, t3 = st.tabs(["🔄 Absorbansi & Transmitansi", "⚗️ Lambert-Beer", "📊 Kurva Kalibrasi"])
    with t1:
        tab_at()
    with t2:
        tab_lb()
    with t3:
        tab_cal()

# ---------------- main ----------------
nav()
st.write("")
{"Home": page_home, "Teori": page_teori, "Model 3D": page_3d, "Perhitungan": page_calc}[st.session_state.page]()
st.markdown('<div class="foot">🔬 <b>UV-Vis Explorer — Virtual Spectrophotometry Laboratory</b><br>'
            'Aplikasi edukasi untuk pembelajaran. Data simulasi bukan hasil pengukuran laboratorium nyata.</div>', unsafe_allow_html=True)
