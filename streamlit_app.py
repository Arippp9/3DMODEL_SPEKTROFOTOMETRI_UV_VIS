
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import numpy as np
import pandas as pd
import math

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="UV-Vis Explorer",
    page_icon="🔬",
    layout="wide"
)

# ==========================================
# DESAIN DAN WARNA TEKS
# ==========================================
st.markdown("""
<style>
/* Latar belakang */
.stApp {
    background-color: #faf9f5;
    color: #111111;
}

/* Area utama */
.block-container {
    max-width: 1200px;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

/* Semua teks utama */
.stApp,
.stApp p,
.stApp span,
.stApp label,
.stApp li,
.stApp small,
.stMarkdown,
.stMarkdown p,
.stMarkdown li,
.stCaption,
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {
    color: #111111;
}

/* Judul */
h1, h2, h3, h4, h5, h6 {
    color: #111111 !important;
}

/* Tab navigasi */
.stTabs [data-baseweb="tab"] {
    color: #111111 !important;
}

.stTabs [aria-selected="true"] {
    color: #111111 !important;
}

/* Label dan input */
.stTextInput label,
.stNumberInput label,
.stSelectbox label,
.stRadio label,
.stSlider label,
.stMultiSelect label {
    color: #111111 !important;
}

/* Nilai input */
.stNumberInput input,
.stTextInput input,
.stTextArea textarea {
    color: #111111 !important;
    background-color: #ffffff !important;
}

/* Pilihan dropdown */
[data-baseweb="select"] * {
    color: #111111 !important;
}

/* Tabel */
[data-testid="stDataFrame"],
[data-testid="stTable"] {
    color: #111111;
}

/* Kotak metrik */
div[data-testid="stMetric"] {
    background-color: #ffffff;
    border: 1px solid #e6e1d8;
    padding: 15px;
    border-radius: 10px;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricValue"],
[data-testid="stMetricDelta"] {
    color: #111111 !important;
}

/* Tombol */
.stButton button {
    color: #111111 !important;
    border: 1px solid #b8b2a8;
}

/* Caption */
.stCaption,
[data-testid="stCaptionContainer"] {
    color: #333333 !important;
}

/* Garis pemisah */
hr {
    border-color: #d8d3ca;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================
st.title("🔬 UV-Vis Explorer")

st.caption(
    "Laboratorium Virtual Spektrofotometri UV-Vis | "
    "Media pembelajaran, simulasi instrumen, dan perhitungan analisis."
)

st.divider()

# ==========================================
# NAVIGASI SECTION
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🏠 Beranda",
    "📘 Teori",
    "🧊 Model 3D",
    "🧮 Perhitungan"
])

# ==========================================
# SECTION 1: BERANDA
# ==========================================
with tab1:
    st.header("Selamat Datang di UV-Vis Explorer")

    st.write("""
    UV-Vis Explorer merupakan media pembelajaran virtual
    untuk memahami prinsip kerja spektrofotometri ultraviolet
    dan cahaya tampak (UV-Vis).

    Melalui aplikasi ini, pengguna dapat mempelajari teori
    dasar, mengamati model instrumen 3D interaktif, serta
    melakukan perhitungan absorbansi, transmitansi,
    dan persamaan Lambert-Beer.
    """)

    st.subheader("Fitur Pembelajaran")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📘 Teori")
        st.write(
            "Pelajari prinsip dasar spektrofotometri UV-Vis, "
            "absorbansi, transmitansi, dan hukum Lambert-Beer."
        )

        st.markdown("### 🧊 Model 3D")
        st.write(
            "Amati model interaktif Shimadzu UV-1700 PharmaSpec "
            "melalui tampilan 3D."
        )

    with col2:
        st.markdown("### 🧮 Perhitungan")
        st.write(
            "Hitung absorbansi, transmitansi, konsentrasi, "
            "dan persamaan regresi kurva kalibrasi."
        )

        st.markdown("### 🎯 Tujuan")
        st.write(
            "Membantu pengguna memahami instrumen dan "
            "penerapan perhitungan dalam analisis UV-Vis."
        )

# ==========================================
# SECTION 2: TEORI
# ==========================================
with tab2:
    st.header("Teori Spektrofotometri UV-Vis")

    st.subheader("1. Pengertian Spektrofotometri UV-Vis")

    st.write("""
    Spektrofotometri UV-Vis adalah metode analisis yang
    mengukur penyerapan radiasi ultraviolet dan cahaya tampak
    oleh suatu zat pada panjang gelombang tertentu.

    Besarnya penyerapan cahaya dapat digunakan untuk
    membantu menentukan konsentrasi analit dalam sampel.
    """)

    st.divider()

    st.subheader("2. Absorbansi")

    st.write("""
    Absorbansi menunjukkan besarnya cahaya yang diserap
    oleh sampel. Absorbansi dapat dihitung berdasarkan
    nilai transmitansi.
    """)

    st.latex(r"A=-\log_{10}(T)")

    st.write(
        "T merupakan transmitansi dalam bentuk pecahan, "
        "bukan persen."
    )

    st.divider()

    st.subheader("3. Transmitansi")

    st.write("""
    Transmitansi merupakan perbandingan intensitas cahaya
    yang melewati sampel terhadap intensitas cahaya datang.
    Nilainya dapat dinyatakan sebagai pecahan atau persen.
    """)

    st.latex(r"\%T=\frac{I}{I_0}\times100\%")

    st.write("""
    Keterangan:
    - I = intensitas cahaya setelah melewati sampel.
    - I₀ = intensitas cahaya sebelum melewati sampel.
    """)

    st.divider()

    st.subheader("4. Hukum Lambert-Beer")

    st.write("""
    Hukum Lambert-Beer menjelaskan hubungan antara
    absorbansi, absorptivitas molar, panjang lintasan optik,
    dan konsentrasi zat penyerap.
    """)

    st.latex(r"A=\varepsilon b c")

    st.write("""
    Keterangan:
    - A = absorbansi.
    - ε = absorptivitas molar.
    - b = panjang lintasan optik.
    - c = konsentrasi larutan.
    """)

    st.divider()

    st.subheader("5. Kurva Kalibrasi")

    st.write("""
    Kurva kalibrasi dibuat dengan mengukur absorbansi
    beberapa larutan standar yang konsentrasinya diketahui.
    Hubungan konsentrasi dan absorbansi dianalisis
    menggunakan regresi linear untuk memperoleh persamaan
    garis dan menentukan konsentrasi sampel.
    """)

    st.latex(r"y=ax+b")

    st.write("""
    Pada kurva kalibrasi, y biasanya menyatakan absorbansi,
    x menyatakan konsentrasi, a merupakan kemiringan garis,
    dan b merupakan intersep.
    """)

# ==========================================
# SECTION 3: MODEL 3D
# ==========================================
with tab3:
    st.header("Shimadzu UV-1700 PharmaSpec")

    st.write("""
    Jelajahi model 3D instrumen spektrofotometer UV-Vis.
    Gunakan kontrol yang tersedia untuk memutar tampilan
    dan mengamati bagian-bagian instrumen.
    """)

    html_path = (
        Path(__file__).parent
        / "UV-1700 PharmaSpec 3D.html"
    )

    if html_path.exists():
        try:
            html_code = html_path.read_text(encoding="utf-8")

            components.html(
                html_code,
                height=800,
                scrolling=True
            )

        except Exception as e:
            st.error(
                f"Terjadi kesalahan saat membaca file HTML: {e}"
            )

    else:
        st.error(
            "File desain 3D tidak ditemukan. "
            "Pastikan file 'UV-1700 PharmaSpec 3D.html' "
            "berada satu folder dengan streamlit_app.py."
        )

    st.caption(
        "Catatan: model merupakan media pembelajaran. "
        "Susunan komponen ilustrasi tidak selalu mewakili "
        "susunan internal instrumen yang sebenarnya."
    )

# ==========================================
# SECTION 4: PERHITUNGAN
# ==========================================
with tab4:
    st.header("Kalkulator Spektrofotometri UV-Vis")

  
# ==========================================
# SECTION 4: KALKULATOR Cr(VI)
# ==========================================
with tab4:
    st.header("Kalkulator Kadar Cr(VI)")

    st.write(
        "Kalkulator penetapan kadar kromium heksavalen "
        "(Cr VI) menggunakan metode spektrofotometri UV-Vis."
    )

    html_path_crvi = Path(__file__).parent / "kalkulator_crvi.html"

    if html_path_crvi.exists():
        html_code_crvi = html_path_crvi.read_text(
            encoding="utf-8"
        )

        components.html(
            html_code_crvi,
            height=1600,
            scrolling=True
        )
    else:
        st.error(
            "File kalkulator_crvi.html tidak ditemukan. "
            "Pastikan file berada satu folder dengan streamlit_app.py."
        )


# ==========================================
# FOOTER
# ==========================================
st.divider()

st.markdown("""
<div style="
    text-align: center;
    color: #333333;
    padding: 12px;
">
    <b>UV-Vis Explorer</b><br>
    Laboratorium Virtual Spektrofotometri UV-Vis<br>
    Media pembelajaran dan simulasi instrumen
</div>
""", unsafe_allow_html=True)
