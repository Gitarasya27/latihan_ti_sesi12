from datetime import datetime
from getpass import getpass
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

# Pengaturan lokasi folder
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

# Membuat folder output jika belum tersedia
OUTPUT_DIR.mkdir(exist_ok=True)

# Tanggal acuan penghitungan retensi
TANGGAL_ACUAN = pd.Timestamp("2026-12-31")
# Blok 1 - Membaca data mentah
file_csv = DATA_DIR / "daftar_arsip_fakultas.csv"

df = pd.read_csv(
    file_csv,
    dtype=str,
    keep_default_na=False
)

print("Ukuran data:", df.shape)
print(df.head())
# Blok 2 - Membersihkan teks
df.columns = df.columns.str.strip()

for kolom in df.select_dtypes(include="object").columns:
    df[kolom] = df[kolom].str.strip()

print("Pembersihan teks selesai.")
# Blok 3 - Normalisasi istilah (controlled vocabulary)

peta_unit = {
    "kepeg": "Kepegawaian",
    "kepegawaian": "Kepegawaian",
    "akademik": "Akademik",
    "kemahasiswaan": "Kemahasiswaan",
    "umum": "Umum dan Perlengkapan",
    "umum dan perlengkapan": "Umum dan Perlengkapan",
    "keuangan": "Keuangan"
}

peta_media = {
    "kertas": "Kertas",
    "digital": "Digital",
    "elektronik": "Digital"
}

peta_akses = {
    "terbuka": "Terbuka",
    "terbatas": "Terbatas",
    "rahasia": "Rahasia"
}

df["unit_pencipta"] = (
    df["unit_pencipta"].str.lower().map(peta_unit)
)

df["media"] = (
    df["media"].str.lower().map(peta_media)
)

df["tingkat_akses"] = (
    df["tingkat_akses"].str.lower().map(peta_akses)
)

print("Normalisasi istilah selesai.")