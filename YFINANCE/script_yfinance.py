# ====== Import Library ======
import pandas as pd
import yfinance as yf
import random
import json
import pymongo

# ====== 1. Load Daftar Saham dari Excel ======
file_path = "D:\\Project\\BIGDATA\\TUGAS\\TUGAS1\\YFINANCE\\Daftar Saham  - 20250226.xlsx"  # Sesuaikan path file
df_tickers = pd.read_excel(file_path)

# Buat list ticker untuk yfinance (.JK untuk saham Indonesia)
ticker_list = df_tickers["Kode"].astype(str) + ".JK"

# Pilih 100 saham secara acak
random.seed(42)  # Agar hasil tetap sama setiap kali dijalankan
selected_tickers = random.sample(list(ticker_list), 100)

print(f"Total saham yang dipilih: {len(selected_tickers)}")
print("5 saham pertama:", selected_tickers[:5])

# ====== 2. Ambil Data Saham dari Yahoo Finance ======
stock_data = {}

for ticker in selected_tickers:
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")  # Ambil data 1 tahun terakhir

        if not hist.empty:
            # Konversi DataFrame ke dictionary
            stock_data[ticker] = hist.reset_index().to_dict(orient='records')
            print(f"Berhasil ambil data {ticker}")
        else:
            print(f"Data kosong untuk {ticker}")

    except Exception as e:
        print(f"Gagal mengambil data {ticker}: {e}")

# Simpan ke file JSON
json_file_path = "stock_data.json"
try:
    with open(json_file_path, 'w') as json_file:
        json.dump(stock_data, json_file, indent=4, default=str)
    print("Data berhasil disimpan ke stock_data.json")
except Exception as e:
    print(f"Gagal menyimpan file JSON: {e}")

# ====== 3. Koneksi ke MongoDB ======
try:
    client = pymongo.MongoClient("mongodb://localhost:27017/")  # Gunakan MongoDB lokal
    db = client["saham_db"]  # Buat atau gunakan database 'saham_db'
    collection = db["stock_data"]  # Buat atau gunakan koleksi 'stock_data'
    print("Koneksi ke MongoDB berhasil!")
except Exception as e:
    print(f"Gagal terhubung ke MongoDB: {e}")

# ====== 4. Baca File JSON & Masukkan ke MongoDB ======
try:
    with open(json_file_path, "r") as json_file:
        stock_data = json.load(json_file)

    for ticker, records in stock_data.items():
        for record in records:
            record["ticker"] = ticker  # Tambahkan field ticker
            collection.insert_one(record)  # Simpan ke MongoDB

    print("Data berhasil dimasukkan ke MongoDB!")
except Exception as e:
    print(f"Gagal memasukkan data ke MongoDB: {e}")

# ====== 5. Cek Data yang Sudah Masuk ======
try:
    print("Contoh data dari MongoDB:")
    for doc in collection.find().limit(5):  # Tampilkan 5 data pertama
        print(doc)
except Exception as e:
    print(f"Gagal mengambil data dari MongoDB: {e}")

