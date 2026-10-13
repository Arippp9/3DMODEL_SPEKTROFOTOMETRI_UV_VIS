
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
# DESAIN TAMPILAN
# ==========================================
st.markdown("""
<style>
.stApp {
    background: #faf9f5;
}

.block-container {
    max-width: 1200px;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    color: #263746;
}

div[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e6e1d8;
    padding: 15px;
    border-radius: 10px;
}

div[data-testid="stTabs"] button {
    font-weight: 600;
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
        "Pada persamaan tersebut, T merupakan transmitansi "
        "dalam bentuk pecahan, bukan persen."
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
    Hubungan konsentrasi dan absorbansi dapat dianalisis
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
    Gunakan kontrol yang tersedia pada model untuk memutar
    tampilan dan mengamati bagian-bagian instrumen.
    """)

    # Nama file HTML harus sama persis dengan file di GitHub
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

        st.info("""
        Periksa nama file di GitHub. Pastikan nama file,
        spasi, dan huruf besar-kecilnya sesuai dengan
        nama yang digunakan dalam kode.
        """)

    st.caption(
        "Catatan: model merupakan media pembelajaran. "
        "Susunan komponen pada ilustrasi 3D tidak selalu "
        "mewakili susunan internal instrumen yang sebenarnya."
    )

# ==========================================
# SECTION 4: PERHITUNGAN
# ==========================================
with tab4:
    st.header("Kalkulator Spektrofotometri UV-Vis")

    subtab1, subtab2, subtab3 = st.tabs([
        "Absorbansi & Transmitansi",
        "Lambert-Beer",
        "Kurva Kalibrasi"
    ])

    # --------------------------------------
    # 4A. ABSORBANSI DAN TRANSMITANSI
    # --------------------------------------
    with subtab1:
        st.subheader("Konversi Absorbansi dan Transmitansi")

        mode = st.radio(
            "Pilih jenis perhitungan:",
            [
                "Transmitansi (%) → Absorbansi",
                "Absorbansi → Transmitansi (%)"
            ],
            horizontal=True
        )

        if mode == "Transmitansi (%) → Absorbansi":
            transmitansi = st.number_input(
                "Transmitansi (%T)",
                min_value=0.000001,
                max_value=100.0,
                value=50.0,
                step=1.0
            )

            if st.button("Hitung Absorbansi"):
                T = transmitansi / 100
                absorbansi = -math.log10(T)

                st.metric(
                    "Nilai Absorbansi",
                    f"{absorbansi:.6f}"
                )

                st.code(
                    f"A = -log10({transmitansi}/100)\n"
                    f"A = {absorbansi:.6f}"
                )

        else:
            absorbansi_input = st.number_input(
                "Absorbansi",
                min_value=0.0,
                value=0.30103,
                step=0.01,
                format="%.6f"
            )

            if st.button("Hitung Transmitansi"):
                transmitansi_hasil = (
                    10 ** (-absorbansi_input)
                ) * 100

                st.metric(
                    "Transmitansi (%T)",
                    f"{transmitansi_hasil:.6f}%"
                )

                st.code(
                    f"%T = 10^(-{absorbansi_input}) × 100\n"
                    f"%T = {transmitansi_hasil:.6f}%"
                )

    # --------------------------------------
    # 4B. HUKUM LAMBERT-BEER
    # --------------------------------------
    with subtab2:
        st.subheader("Perhitungan Hukum Lambert-Beer")

        st.latex(r"A=\varepsilon b c")

        pilihan = st.selectbox(
            "Besaran yang ingin dihitung:",
            [
                "Konsentrasi (c)",
                "Absorbansi (A)",
                "Absorptivitas molar (ε)"
            ]
        )

        col1, col2 = st.columns(2)

        with col1:
            A_input = st.number_input(
                "Absorbansi (A)",
                min_value=0.0,
                value=0.5,
                step=0.1
            )

            epsilon_input = st.number_input(
                "Absorptivitas molar (ε)",
                min_value=0.000001,
                value=1000.0,
                step=100.0
            )

        with col2:
            b_input = st.number_input(
                "Panjang lintasan optik (b)",
                min_value=0.000001,
                value=1.0,
                step=0.1
            )

            c_input = st.number_input(
                "Konsentrasi (c)",
                min_value=0.0,
                value=0.0005,
                format="%.8f"
            )

        if st.button("Hitung Lambert-Beer"):
            if pilihan == "Konsentrasi (c)":
                hasil = A_input / (epsilon_input * b_input)

                st.metric(
                    "Konsentrasi (c)",
                    f"{hasil:.8g}"
                )

                st.code(
                    f"c = A / (ε × b)\n"
                    f"c = {A_input} / "
                    f"({epsilon_input} × {b_input})\n"
                    f"c = {hasil:.8g}"
                )

            elif pilihan == "Absorbansi (A)":
                hasil = epsilon_input * b_input * c_input

                st.metric(
                    "Absorbansi (A)",
                    f"{hasil:.8g}"
                )

                st.code(
                    f"A = ε × b × c\n"
                    f"A = {epsilon_input} × "
                    f"{b_input} × {c_input}\n"
                    f"A = {hasil:.8g}"
                )

            else:
                if b_input * c_input == 0:
                    st.error(
                        "Panjang lintasan optik dan konsentrasi "
                        "tidak boleh menghasilkan penyebut nol."
                    )
                else:
                    hasil = A_input / (b_input * c_input)

                    st.metric(
                        "Absorptivitas molar (ε)",
                        f"{hasil:.8g}"
                    )

                    st.code(
                        f"ε = A / (b × c)\n"
                        f"ε = {A_input} / "
                        f"({b_input} × {c_input})\n"
                        f"ε = {hasil:.8g}"
                    )

        st.info(
            "Pastikan satuan ε, b, dan c konsisten "
            "dengan sistem satuan yang digunakan."
        )

    # --------------------------------------
    # 4C. KURVA KALIBRASI DAN REGRESI LINEAR
    # --------------------------------------
    with subtab3:
        st.subheader("Regresi Linear Kurva Kalibrasi")

        st.write("""
        Masukkan data konsentrasi larutan standar dan
        absorbansinya. Kamu bisa mengedit tabel secara langsung.
        """)

        data_awal = pd.DataFrame({
            "Konsentrasi": [1.0, 2.0, 3.0, 4.0, 5.0],
            "Absorbansi": [0.10, 0.21, 0.31, 0.40, 0.52]
        })

        data = st.data_editor(
            data_awal,
            num_rows="dynamic",
            use_container_width=True,
            key="tabel_kalibrasi"
        )

        if st.button("Hitung Regresi Linear"):
            data_bersih = data[
                ["Konsentrasi", "Absorbansi"]
            ].dropna()

            if len(data_bersih) < 2:
                st.error(
                    "Masukkan minimal dua pasangan data "
                    "konsentrasi dan absorbansi."
                )

            elif (
                data_bersih["Konsentrasi"].nunique() < 2
            ):
                st.error(
                    "Nilai konsentrasi harus memiliki "
                    "minimal dua nilai yang berbeda."
                )

            else:
                x = data_bersih[
                    "Konsentrasi"
                ].to_numpy(dtype=float)

                y = data_bersih[
                    "Absorbansi"
                ].to_numpy(dtype=float)

                if not (
                    np.isfinite(x).all()
                    and np.isfinite(y).all()
                ):
                    st.error(
                        "Data harus berupa angka yang valid."
                    )

                else:
                    slope, intercept = np.polyfit(x, y, 1)

                    y_prediksi = slope * x + intercept

                    ss_res = np.sum(
                        (y - y_prediksi) ** 2
                    )

                    ss_tot = np.sum(
                        (y - np.mean(y)) ** 2
                    )

                    if ss_tot == 0:
                        r_squared = float("nan")
                    else:
                        r_squared = 1 - ss_res / ss_tot

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric(
                            "Slope (a)",
                            f"{slope:.6f}"
                        )

                    with col2:
                        st.metric(
                            "Intersep (b)",
                            f"{intercept:.6f}"
                        )

                    with col3:
                        st.metric(
                            "R²",
                            f"{r_squared:.6f}"
                        )

                    st.markdown("### Persamaan Regresi")

                    st.code(
                        f"y = {slope:.6f}x "
                        f"+ ({intercept:.6f})"
                    )

                    st.write(
                        "Koefisien determinasi (R²): "
                        f"{r_squared:.6f}"
                    )

                    hasil_tabel = data_bersih.copy()

                    hasil_tabel[
                        "Absorbansi Prediksi"
                    ] = y_prediksi

                    st.markdown("### Hasil Perhitungan")

                    st.dataframe(
                        hasil_tabel,
                        use_container_width=True
                    )

                    st.caption("""
                    R² menunjukkan seberapa baik data
                    mengikuti model linear. Nilai R² yang
                    tinggi saja tidak cukup untuk memastikan
                    bahwa seluruh persyaratan validasi metode
                    telah terpenuhi.
                    """)

# ==========================================
# FOOTER
# ==========================================
st.divider()

st.markdown("""
<div style="
    text-align: center;
    color: #777;
    padding: 12px;
">
    <b>UV-Vis Explorer</b><br>
    Laboratorium Virtual Spektrofotometri UV-Vis<br>
    Media pembelajaran dan simulasi instrumen
</div>
""", unsafe_allow_html=True)
