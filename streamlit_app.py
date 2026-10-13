
import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
import math
from pathlib import Path

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
    background: red;
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
        raise ValueError(
            "Transmitansi harus lebih dari 0 sampai 1."
        )
    return -math.log10(T)


def hitung_transmitansi(A):
    if not math.isfinite(A) or A < 0:
        raise ValueError(
            "Absorbansi tidak boleh negatif."
        )
    return 10 ** (-A)


def hitung_konsentrasi(A, epsilon, b):
    if epsilon <= 0 or b <= 0:
        raise ValueError(
            "Nilai epsilon dan panjang lintasan harus lebih dari 0."
        )
    if A < 0:
        raise ValueError(
            "Absorbansi tidak boleh negatif."
        )
    return A / (epsilon * b)


# =========================
# MODEL 3D SPEKTROFOTOMETER
# =========================
# Konfigurasi halaman
elif halaman == "Model 3D":

st.set_page_config(
    page_title="UV-1700 PharmaSpec 3D",
    page_icon="🔬",
    layout="wide"
)

# Desain tampilan Streamlit
st.markdown("""
<style>
.stApp {
    background: #faf9f5;
}

.block-container {
    max-width: 1100px;
    padding-top: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

# Judul halaman
st.title("🔬 Shimadzu UV-1700 PharmaSpec")

st.caption(
    "Model 3D interaktif spektrofotometer UV-Vis. "
    "Putar model, amati bagian luar dan dalam, "
    "serta pelajari fungsi komponen."
)

# Lokasi file desain 3D HTML
html_path = Path(__file__).parent / "UV-1700 PharmaSpec 3D.html"

# Memuat desain 3D
if html_path.exists():
    try:
        html_code = html_path.read_text(encoding="utf-8")

        components.html(
            html_code,
            height=760,
            scrolling=True
        )

    except Exception as e:
        st.error(f"Gagal membaca file HTML: {e}")

else:
    st.error(
        "File desain 3D tidak ditemukan. "
        "Pastikan file bernama "
        "'UV-1700 PharmaSpec 3D.html' "
        "berada satu folder dengan streamlit_app.py."
    )

# Garis pemisah
st.divider()

# Footer
st.markdown("""
<div style="text-align:center;color:#777;padding:12px">
    <b>UV-Vis Explorer</b><br>
    Laboratorium Virtual Spektrofotometri UV-Vis<br>
    Media pembelajaran dan simulasi instrumen
</div>
""", unsafe_allow_html=True)

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

for col, nama in zip(
    menu, ["Home", "Teori", "Model 3D", "Perhitungan"]
):
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

    st.markdown(
        '<div class="section-title">Menu Utama</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="card">
        <h2>📘 Teori</h2>
        Pelajari prinsip absorpsi cahaya, komponen alat, dan Hukum Lambert-Beer.
        </div>
        """, unsafe_allow_html=True)

        if st.button("Pelajari Teori →", use_container_width=True):
            st.session_state.halaman = "Teori"
            st.rerun()

    with c2:
        st.markdown("""
        <div class="card">
        <h2>🧊 Model 3D</h2>
        Jelajahi bagian spektrofotometer melalui model interaktif.
        </div>
        """, unsafe_allow_html=True)

        if st.button("Buka Model 3D →", use_container_width=True):
            st.session_state.halaman = "Model 3D"
            st.rerun()

    with c3:
        st.markdown("""
        <div class="card">
        <h2>🧮 Perhitungan</h2>
        Hitung absorbansi, transmitansi, konsentrasi, dan kurva kalibrasi.
        </div>
        """, unsafe_allow_html=True)

        if st.button("Mulai Perhitungan →", use_container_width=True):
            st.session_state.halaman = "Perhitungan"
            st.rerun()

    st.info(
        "Aplikasi ini merupakan media pembelajaran. "
        "Gunakan data hasil praktikum untuk analisis nyata."
    )


# =========================
# TEORI
# =========================
elif halaman == "Teori":

    st.markdown(
        '<div class="section-title">Pengertian Spektrofotometri UV-Vis</div>',
        unsafe_allow_html=True
    )

    st.write("""
    Spektrofotometri UV-Vis merupakan metode analisis instrumental yang
    mengukur penyerapan radiasi ultraviolet dan cahaya tampak oleh suatu
    zat. Metode ini dapat digunakan untuk menentukan konsentrasi analit
    berdasarkan hubungan antara absorbansi dan konsentrasi.
    """)

    st.markdown(
        '<div class="section-title">Prinsip Dasar</div>',
        unsafe_allow_html=True
    )

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
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Komponen Instrumen</div>',
        unsafe_allow_html=True
    )

    komponen = {
        "Sumber cahaya":
            "Menghasilkan radiasi UV dan cahaya tampak.",
        "Monokromator":
            "Memisahkan cahaya dan memilih panjang gelombang tertentu.",
        "Celah optik":
            "Mengatur lebar berkas cahaya yang melewati sistem optik.",
        "Kuvet":
            "Menampung larutan sampel pada lintasan cahaya.",
        "Detektor":
            "Mengubah intensitas cahaya menjadi sinyal listrik.",
        "Pengolah sinyal":
            "Menghitung dan mengolah sinyal pengukuran.",
        "Layar":
            "Menampilkan nilai absorbansi, transmitansi, atau spektrum."
    }

    for nama, fungsi in komponen.items():
        with st.expander(nama):
            st.write(fungsi)

    st.markdown(
        '<div class="section-title">Hukum Lambert-Beer</div>',
        unsafe_allow_html=True
    )

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
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Alur Kerja</div>',
        unsafe_allow_html=True
    )

    st.write("""
    Sumber cahaya → Monokromator → Kuvet berisi sampel → Detektor →
    Pengolah sinyal → Hasil pengukuran.
    """)

    st.markdown(
        '<div class="section-title">Faktor yang Memengaruhi Hasil</div>',
        unsafe_allow_html=True
    )

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

    st.markdown(
        '<div class="section-title">Model 3D Spektrofotometer UV-Vis</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="note">
    🖱️ Seret model untuk memutar. Gunakan scroll untuk zoom.
    Klik komponen untuk membaca fungsinya, dan gunakan tombol untuk
    menampilkan jalur cahaya atau membuka tutup kompartemen.
    </div>
    """, unsafe_allow_html=True)

    components.html(MODEL_3D, height=600, scrolling=False)

    st.caption(
        "Model 3D ini merupakan ilustrasi edukasi, "
        "bukan replika instrumen dari merek tertentu."
    )


# =========================
# PERHITUNGAN
# =========================
elif halaman == "Perhitungan":

    st.markdown(
        '<div class="section-title">Kalkulator Spektrofotometri</div>',
        unsafe_allow_html=True
    )

    tab1, tab2, tab3 = st.tabs([
        "Absorbansi & Transmitansi",
        "Lambert-Beer",
        "Kurva Kalibrasi"
    ])

    # -------------------------
    # ABSORBANSI & TRANSMITANSI
    # -------------------------
    with tab1:
        st.subheader("Konversi Absorbansi dan Transmitansi")

        pilihan = st.radio(
            "Pilih data yang diketahui",
            [
                "Transmitansi (T)",
                "Persen transmitansi (%T)",
                "Absorbansi (A)"
            ],
            horizontal=True
        )

        nilai = st.number_input(
            "Masukkan nilai",
            value=0.5,
            step=0.01,
            format="%.5f"
        )

        if st.button("Hitung", key="hitung_at"):
            try:
                if pilihan == "Transmitansi (T)":
                    T = nilai
                    A = hitung_absorbansi(T)

                elif pilihan == "Persen transmitansi (%T)":
                    if nilai <= 0 or nilai > 100:
                        raise ValueError(
                            "%T harus lebih dari 0 sampai 100."
                        )
                    T = nilai / 100
                    A = hitung_absorbansi(T)

                else:
                    A = nilai
                    T = hitung_transmitansi(A)

                c1, c2, c3 = st.columns(3)
                c1.metric("Absorbansi", f"{A:.5f}")
                c2.metric("Transmitansi", f"{T:.6f}")
                c3.metric("Transmitansi (%)", f"{T*100:.3f}%")

                st.latex(r"A=-\log_{10}(T)")
                st.write(
                    f"A = −log₁₀({T:.6f}) = {A:.5f}"
                )

            except ValueError as e:
                st.error(str(e))

    # -------------------------
    # LAMBERT-BEER
    # -------------------------
    with tab2:
        st.subheader("Menghitung Konsentrasi")

        st.latex(r"c=\frac{A}{\varepsilon b}")

        col1, col2, col3 = st.columns(3)

        with col1:
            A = st.number_input(
                "Absorbansi (A)",
                min_value=0.0,
                value=0.450,
                step=0.01
            )

        with col2:
            epsilon = st.number_input(
                "ε (L mol⁻¹ cm⁻¹)",
                min_value=0.000001,
                value=12000.0,
                step=100.0
            )

        with col3:
            b = st.number_input(
                "Panjang lintasan (cm)",
                min_value=0.000001,
                value=1.0,
                step=0.1
            )

        if st.button("Hitung Konsentrasi"):
            try:
                c = hitung_konsentrasi(A, epsilon, b)

                st.success(
                    f"Konsentrasi = {c:.5e} mol/L"
                )
                st.write(
                    f"Konsentrasi = {c*1000:.5f} mmol/L"
                )
                st.write("Langkah perhitungan:")
                st.write("c = A / (ε × b)")
                st.write(f"c = {A} / ({epsilon} × {b})")
                st.write(f"c = {c:.5e} mol/L")

            except ValueError as e:
                st.error(str(e))

    # -------------------------
    # KURVA KALIBRASI
    # Tanpa grafik Plotly
    # -------------------------
    with tab3:
        st.subheader("Perhitungan Kurva Kalibrasi")

        st.info(
            "Data berikut adalah data simulasi untuk latihan. "
            "Ganti dengan data hasil praktikum."
        )

        data_awal = pd.DataFrame({
            "Konsentrasi (mg/L)": [0, 2, 4, 6, 8, 10],
            "Absorbansi": [
                0.002, 0.101, 0.205, 0.298, 0.405, 0.502
            ]
        })

        data = st.data_editor(
            data_awal,
            num_rows="dynamic",
            use_container_width=True,
            key="tabel_kalibrasi"
        )

        A_sampel = st.number_input(
            "Absorbansi sampel",
            value=0.350,
            step=0.01
        )

        if st.button("Hitung Kurva Kalibrasi"):
            try:
                d = data.apply(
                    pd.to_numeric, errors="coerce"
                ).dropna()

                if len(d) < 3:
                    raise ValueError(
                        "Masukkan minimal 3 baris data yang lengkap."
                    )

                x = d.iloc[:, 0].to_numpy(dtype=float)
                y = d.iloc[:, 1].to_numpy(dtype=float)

                if not np.all(np.isfinite(x)) or not np.all(np.isfinite(y)):
                    raise ValueError(
                        "Data harus berupa angka yang valid."
                    )

                if np.any(x < 0):
                    raise ValueError(
                        "Konsentrasi tidak boleh negatif."
                    )

                if np.any(y < 0):
                    raise ValueError(
                        "Absorbansi tidak boleh negatif."
                    )

                if len(np.unique(x)) < 2:
                    raise ValueError(
                        "Gunakan konsentrasi yang berbeda."
                    )

                m, b0 = np.polyfit(x, y, 1)
                pred = m * x + b0

                ss_res = np.sum((y - pred) ** 2)
                ss_tot = np.sum((y - np.mean(y)) ** 2)
                r2 = (
                    1 - ss_res / ss_tot
                    if ss_tot != 0 else 1.0
                )

                st.markdown("### Hasil Regresi Linear")

                st.metric(
                    "Persamaan regresi",
                    f"y = {m:.5f}x + ({b0:.5f})"
                )

                st.metric(
                    "Koefisien determinasi (R²)",
                    f"{r2:.5f}"
                )

                st.write(
                    "Keterangan: y adalah absorbansi, x adalah "
                    "konsentrasi, m adalah kemiringan garis, "
                    "dan b adalah intersep."
                )

                if abs(m) < 1e-12:
                    raise ValueError(
                        "Kemiringan garis terlalu kecil "
                        "untuk menghitung konsentrasi."
                    )

                konsentrasi = (A_sampel - b0) / m

                st.markdown("### Hasil Analisis Sampel")
                st.write(f"Absorbansi sampel = {A_sampel:.5f}")
                st.write("Konsentrasi = (A - b) / m")
                st.write(
                    f"Konsentrasi = ({A_sampel:.5f} - "
                    f"({b0:.5f})) / {m:.5f}"
                )

                st.success(
                    f"Perkiraan konsentrasi sampel = "
                    f"{konsentrasi:.4f} mg/L"
                )

                if r2 < 0.99:
                    st.warning(
                        "R² kurang dari 0,99. Periksa kembali "
                        "data dan linearitas kurva."
                    )

                if (
                    konsentrasi < np.min(x)
                    or konsentrasi > np.max(x)
                ):
                    st.warning(
                        "Konsentrasi sampel berada di luar "
                        "rentang standar. Hasil merupakan ekstrapolasi."
                    )

            except (
                ValueError,
                TypeError,
                np.linalg.LinAlgError
            ) as e:
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
""", unsafe_allow_html=True)
