# 🔬 UV-Vis Explorer — Virtual Spectrophotometry Laboratory

Aplikasi edukasi interaktif (Python + Streamlit) untuk mempelajari spektrofotometri UV-Vis: teori, model 3D instrumen, dan kalkulator.

## Fitur
- **Home**: landing page, navigasi, kartu menu.
- **Teori**: 8 subbagian (prinsip absorpsi, rentang UV-Vis, komponen alat, alur kerja, blanko/λmaks, Hukum Lambert-Beer, keterbatasan).
- **Model 3D** (Three.js): rotasi 360°, zoom, pilihan sudut pandang, reset, buka/tutup kompartemen kuvet, klik komponen + panel info + highlight + label, animasi jalur cahaya, mode tembus, fallback bila CDN gagal.
- **Perhitungan**: (1) konversi A ↔ T ↔ %T, (2) konsentrasi c = A/(εb), (3) kurva kalibrasi Plotly dengan regresi linear, R², dan estimasi konsentrasi sampel.
- Data awal kalibrasi adalah **simulasi**, bukan hasil pengukuran laboratorium nyata.

## Struktur
```
app.py            # tampilan & navigasi
calc.py           # logika perhitungan
viewer.py         # komponen 3D (HTML + Three.js)
requirements.txt
.streamlit/config.toml
assets/
```

## Menjalankan secara lokal
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
Buka http://localhost:8501. Model 3D memerlukan koneksi internet (Three.js dimuat dari CDN).

## Mengunggah ke GitHub
```bash
git init
git add .
git commit -m "UV-Vis Explorer"
git branch -M main
git remote add origin https://github.com/USERNAME/uvvis-explorer.git
git push -u origin main
```

## Deploy di Streamlit Community Cloud
1. Buka https://share.streamlit.io lalu masuk dengan akun GitHub.
2. Klik **Create app** → pilih repository `uvvis-explorer`.
3. Branch: `main`; Main file path: `app.py`.
4. Klik **Deploy**. Dependensi dibaca otomatis dari `requirements.txt`.

## Memperbarui aplikasi
```bash
git add .
git commit -m "Perbarui aplikasi"
git push
```
Streamlit Community Cloud otomatis memuat ulang aplikasi setelah push.

## Catatan
Aplikasi ini bersifat edukasi. Model 3D adalah visualisasi dari bentuk dasar, bukan gambar pasti instrumen komersial tertentu.
