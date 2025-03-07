import pandas as pd

# Load daftar saham dari file Excel
file_path = "Daftar Saham  - 20250226.xlsx"

# Pastikan membaca file dengan benar
df_tickers = pd.read_excel(file_path)

# Cek apakah kolom "Kode" ada dalam file
if "Kode" in df_tickers.columns:
    # Ambil daftar kode saham (pastikan format string, hilangkan NaN)
    kode_saham_list = df_tickers["Kode"].dropna().astype(str).tolist()

    # Cek 5 kode pertama
    print("5 kode saham pertama:", kode_saham_list[:5])
else:
    print("Kolom 'Kode' tidak ditemukan dalam file.")
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
    
import os
import shutil
import zipfile
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Load daftar saham dari Excel
file_path = "Daftar Saham  - 20250226.xlsx"
df_tickers = pd.read_excel(file_path)

if "Kode" in df_tickers.columns:
    kode_saham_list = df_tickers["Kode"].dropna().astype(str).tolist()
else:
    raise ValueError("Kolom 'Kode' tidak ditemukan dalam file.")

# Path penyimpanan utama
base_download_dir = r"C:\Users\Lenovo\OneDrive\Dokumen\Coding\Semester 4\Big Data Platforms\Tugas 1\Laporan_Keuangan"
os.makedirs(base_download_dir, exist_ok=True)  # Pastikan folder utama ada

# Setup Chrome dengan custom folder download
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": base_download_dir,
    "download.prompt_for_download": False,  # Jangan munculkan pop-up download
    "download.directory_upgrade": True
})

# Start WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Base URL instance.zip dari IDX
base_url = "https://www.idx.co.id/Portals/0/StaticData/ListedCompanies/Corporate_Actions/New_Info_JSX/Jenis_Informasi/01_Laporan_Keuangan/02_Soft_Copy_Laporan_Keuangan/Laporan%20Keuangan%20Tahun%202024/Audit/{}/instance.zip"

# List untuk menyimpan kode saham yang berhasil di-download & diekstrak
downloaded_tickers = []

for kode in kode_saham_list:
    # Buat folder khusus untuk tiap saham
    saham_folder = os.path.join(base_download_dir, kode)
    os.makedirs(saham_folder, exist_ok=True)  

    # Set folder download ke dalam folder khusus
    driver.execute_cdp_cmd("Page.setDownloadBehavior", {
        "behavior": "allow",
        "downloadPath": saham_folder
    })

    url = base_url.format(kode)
    driver.get(url)
    time.sleep(5)  # Tunggu sebentar agar file mulai ter-download

    zip_path = os.path.join(saham_folder, "instance.zip")

    if os.path.exists(zip_path):  
        # Ekstrak zip jika file ditemukan
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(saham_folder)

        os.remove(zip_path)  # Hapus file zip setelah ekstrak
        downloaded_tickers.append(kode)  # Simpan kode saham yang berhasil

        print(f"✅ {kode}: Berhasil di-download & diekstrak ke {saham_folder}")
    else:
        # Jika tidak ada file zip, hapus folder emiten
        shutil.rmtree(saham_folder)
        print(f"❌ {kode}: File tidak ditemukan, folder dihapus.")

driver.quit()

# Print daftar kode saham yang berhasil di-download
print("\n Kode saham yang berhasil di-download & diekstrak:")
print(downloaded_tickers)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Debug: Cek file instance.xbrl
for kode in downloaded_tickers:
    saham_folder = os.path.join(base_download_dir, kode)
    xbrl_path = os.path.join(saham_folder, "instance.xbrl")

    print(f"\n🔍 Mengecek file untuk {kode}...")

    # Cek apakah file ada
    if os.path.exists(xbrl_path):
        print(f"✅ {kode}: File instance.xbrl ditemukan!")

        # Coba baca file
        try:
            with open(xbrl_path, "r", encoding="utf-8") as file:
                content = file.readlines()[:5]  # Ambil 10 baris pertama
                print(f"📄 Isi awal file {kode}:\n" + "".join(content))
        except Exception as e:
            print(f"❌ ERROR membaca file {kode}: {e}")
    else:
        print(f"❌ {kode}: File instance.xbrl TIDAK ditemukan!")
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Path utama
base_download_dir = r"C:\Users\Lenovo\OneDrive\Dokumen\Coding\Semester 4\Big Data Platforms\Tugas 1\Laporan_Keuangan"

# Cek folder emiten yang ada
folders = [f for f in os.listdir(base_download_dir) if os.path.isdir(os.path.join(base_download_dir, f))]
downloaded_tickers = folders

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import pymongo
from bs4 import BeautifulSoup

# 📂 Path ke folder laporan keuangan
base_download_dir = r"C:\Users\Lenovo\OneDrive\Dokumen\Coding\Semester 4\Big Data Platforms\Tugas 1\Laporan_Keuangan"

# 📌 Koneksi MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["laporan_keuangan"]
collection = db["xbrl_data"]

# 🔄 Loop semua emiten
folders = [f for f in os.listdir(base_download_dir) if os.path.isdir(os.path.join(base_download_dir, f))]

print("📂 Emiten yang diproses:", folders)

for kode in folders:
    emiten_folder = os.path.join(base_download_dir, kode)
    xbrl_files = [f for f in os.listdir(emiten_folder) if f.endswith(".xbrl")]

    if not xbrl_files:
        print(f"❌ Tidak ada file XBRL di {kode}")
        continue

    file_path = os.path.join(emiten_folder, xbrl_files[0])
    print(f"\n📄 Memproses {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "xml")

        # 🔍 Ambil semua tag dan atribut
        emiten_data = {"kode_emiten": kode, "data": []}
        for tag in soup.find_all():
            tag_info = {
                "tag_name": tag.name,
                "text": tag.text.strip(),
                "attributes": tag.attrs  # Ambil semua atribut dalam bentuk dict
            }
            emiten_data["data"].append(tag_info)

        # 🚀 Insert ke MongoDB
        collection.insert_one(emiten_data)
        print(f"✅ Data {kode} berhasil dimasukkan ke MongoDB!")

    except Exception as e:
        print(f"⚠️ Gagal memproses {kode}: {e}")
