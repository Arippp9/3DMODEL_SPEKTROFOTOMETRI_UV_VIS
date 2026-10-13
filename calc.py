"""Logika perhitungan spektrofotometri UV-Vis (terpisah dari tampilan)."""
import math
import numpy as np


def absorbance_from_T(T: float) -> float:
    """A = -log10(T), T fraksi (0 < T <= 1)."""
    if not math.isfinite(T) or T <= 0 or T > 1:
        raise ValueError("Transmitansi fraksi harus 0 < T ≤ 1 (T = 0 membuat log tak terhingga).")
    return -math.log10(T)


def T_from_absorbance(A: float) -> float:
    """T = 10^(-A)."""
    if not math.isfinite(A) or A < 0:
        raise ValueError("Absorbansi harus berupa angka ≥ 0.")
    return 10 ** (-A)


def percent_from_T(T: float) -> float:
    return 100.0 * T


def T_from_percent(p: float) -> float:
    if not math.isfinite(p) or p <= 0 or p > 100:
        raise ValueError("%T harus 0 < %T ≤ 100.")
    return p / 100.0


def convert(mode: str, value: float) -> dict:
    """mode: 'T', 'P' (persen), atau 'A'. Mengembalikan A, T, %T."""
    if mode == "T":
        T = value
        A = absorbance_from_T(T)
    elif mode == "P":
        T = T_from_percent(value)
        A = absorbance_from_T(T)
    else:
        A = value
        T = T_from_absorbance(A)
    return {"A": A, "T": T, "P": percent_from_T(T)}


def concentration(A: float, eps: float, b: float) -> float:
    """c = A / (ε b)."""
    if not all(map(math.isfinite, (A, eps, b))):
        raise ValueError("Semua input harus berupa angka valid.")
    if A < 0:
        raise ValueError("Absorbansi tidak boleh negatif.")
    if eps <= 0:
        raise ValueError("Absorptivitas molar ε harus > 0.")
    if b <= 0:
        raise ValueError("Panjang lintasan b harus > 0.")
    return A / (eps * b)


def clean_calibration(df):
    """Bersihkan tabel kalibrasi -> (x, y) array. Raise ValueError bila tidak valid."""
    import pandas as pd
    if df is None or len(df.columns) < 2:
        raise ValueError("Tabel kalibrasi harus memiliki dua kolom.")
    d = df.iloc[:, :2].apply(pd.to_numeric, errors="coerce").dropna()
    if len(d) < 3:
        raise ValueError("Minimal 3 titik data numerik yang lengkap diperlukan untuk regresi.")
    x, y = d.iloc[:, 0].to_numpy(float), d.iloc[:, 1].to_numpy(float)
    if np.any(x < 0):
        raise ValueError("Konsentrasi tidak boleh negatif.")
    if np.ptp(x) == 0:
        raise ValueError("Semua konsentrasi sama; regresi tidak dapat dihitung (pembagian dengan nol).")
    return x, y


def linear_regression(x, y) -> dict:
    """y = m x + b dan R²."""
    m, b = np.polyfit(x, y, 1)
    yhat = m * x + b
    ss_res = float(np.sum((y - yhat) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 if ss_tot == 0 else 1 - ss_res / ss_tot
    return {"m": float(m), "b": float(b), "r2": r2, "n": len(x)}


def predict_concentration(A: float, m: float, b: float) -> float:
    """x = (A - b) / m."""
    if not math.isfinite(A):
        raise ValueError("Absorbansi sampel harus berupa angka valid.")
    if abs(m) < 1e-12:
        raise ValueError("Slope ≈ 0, konsentrasi tidak dapat dihitung (pembagian dengan nol).")
    return (A - b) / m
