# Tugas1-BIGDATA

-LAPORAN INGESTION DATA YFINANCE
Proses ingestion data dari Yahoo Finance dilakukan untuk mengumpulkan data harga saham secara historis, dan menyimpannya ke dalam MongoDB. Tahapan yang dilakukan:

Mengambil Daftar Saham dari Excel
Membaca file Excel menggunakan pandas.
Mengonversi kode saham ke format .JK (untuk saham Indonesia).
Memilih 100 saham secara acak.

Mengambil Data Saham
Menggunakan library yfinance untuk mengambil data historis selama satu tahun terakhir.
Data dikonversi ke format dictionary untuk memudahkan konversi ke JSON.

Penyimpanan Data
Menyimpan data saham ke file stock_data.json sebagai cadangan.
Data dimasukkan ke MongoDB (saham_db, koleksi stock_data) menggunakan pymongo.
