import pandas as pd
import numpy as np
import os

# KONFIGURASI FILE
INPUT_FILE = 'data/raw/car_sales.csv' 
OUTPUT_FILE = 'data/processed/cleaned_car_sales_data.csv'

# 1. LOAD DATA
print(f"Membaca data dari: {INPUT_FILE} ...")
# encoding='latin1' wajib dipakai untuk dataset ini
df = pd.read_csv(INPUT_FILE, encoding='latin1') 
print(f"Data dimuat: {df.shape[0]} baris.")

# 2. DATA CLEANING

# A. Cleaning Date
# Mengubah format tanggal agar bisa dibaca SQL/Excel sebagai tanggal
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# B. Cleaning Engine (Timpa Kolom Lama)
def clean_engine_type(value):
    text = str(value)
    if "Double" in text:
        return "Double Overhead Camshaft"
    elif "Overhead" in text:
        return "Overhead Camshaft"
    else:
        return "Unknown"

# Kita timpa kolom 'Engine' yang kotor dengan versi bersih
df['Engine'] = df['Engine'].apply(clean_engine_type)
# Rename jadi Engine_Type biar standar
df.rename(columns={'Engine': 'Engine_Type'}, inplace=True)

# C. Cleaning & Renaming Kolom PRICE
# Nama kolom aslinya "Price ($)". Spasi dan simbol ($) tidak bagus buat SQL.
# Kita cari kolom yang mengandung kata "Price" lalu rename.
for col in df.columns:
    if "Price" in col:
        print(f"Renaming column '{col}' to 'Selling_Price'...")
        df.rename(columns={col: 'Selling_Price'}, inplace=True)

# Pastikan Selling_Price formatnya angka (Int), kadang dataset baca sebagai string
# Kita buang simbol $ atau koma jika ada
if df['Selling_Price'].dtype == 'O': # Kalau tipe datanya Object (String)
    df['Selling_Price'] = df['Selling_Price'].astype(str).str.replace(r'[$,]', '', regex=True)
    df['Selling_Price'] = pd.to_numeric(df['Selling_Price'])

# ==========================================
# 3. DATA ENRICHMENT (Hanya Profit)
# ==========================================

# Kita tidak perlu price_map lagi karena harga sudah ada di dataset!
# Kita hanya perlu hitung PROFIT berdasarkan Harga Asli tersebut.

# Logika: Profit Margin acak antara 5% - 15%
np.random.seed(42) # Biar angkanya konsisten tiap kali run (opsional)
profit_margins = np.random.uniform(0.05, 0.15, size=len(df))

# Hitung Profit = Harga Asli * Margin
df['Profit'] = (df['Selling_Price'] * profit_margins).astype(int)

# ==========================================
# 4. EXPORT FINAL
# ==========================================
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False)

print("\n" + "="*40)
print(f"SUKSES! File bersih tersimpan di:\n{OUTPUT_FILE}")
print("="*40)

# Preview Akhir
print("\nPreview Data (Perhatikan kolom Selling_Price asli & Profit):")
print(df[['Company', 'Model', 'Engine_Type', 'Selling_Price', 'Profit']].head())

