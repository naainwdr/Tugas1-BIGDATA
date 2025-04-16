# Tugas1-BIGDATA

LAPORAN INGESTION DATA YFINANCE
---
Proses ingestion data dari Yahoo Finance dilakukan untuk mengumpulkan data harga saham secara historis, dan menyimpannya ke dalam MongoDB. Tahapan yang dilakukan:

---
1. Mengambil Daftar Saham dari Excel
- Membaca file Excel menggunakan pandas.
- Mengonversi kode saham ke format .JK (untuk saham Indonesia).
- Memilih 100 saham secara acak.
---
2. Mengambil Data Saham
- Menggunakan library yfinance untuk mengambil data historis selama satu tahun terakhir.
- Data dikonversi ke format dictionary untuk memudahkan konversi ke JSON.
---
3. Penyimpanan Data
- Menyimpan data saham ke file stock_data.json sebagai cadangan.
- Data dimasukkan ke MongoDB (saham_db, koleksi stock_data) menggunakan pymongo.

LAPORAN INGESTION DATA IDX
---
Proses ini bertujuan mengunduh laporan keuangan emiten dari situs IDX secara otomatis dan menyimpannya ke MongoDB. Langkah-langkahnya:

---
1. Membaca Daftar Saham
- Mengimpor file Excel dan mengambil kolom kode saham

2. Membuat Folder Simpanan
- Membuat folder utama dan subfolder berdasarkan kode saham.

3. Mengatur WebDriver
- Menggunakan Selenium dan Chrome dalam mode otomatis (tanpa membuka browser).
- Mengatur lokasi unduhan otomatis sesuai folder saham.

4. Mengunduh dan Mengekstrak File ZIP
- Akses URL laporan keuangan dan unduh file ZIP.
- Mengekstrak file instance.xbrl.

5. Proses dan Simpan Data
- Menggunakan BeautifulSoup untuk memproses file xbrl.
- Menyimpan hasil ekstraksi ke MongoDB (saham_db, koleksi sesuai struktur).

LAPORAN INGESTION DATA BERITA IQPLUS
---
Proses ini bertujuan untuk mengambil berita saham dari situs IQPlus dan menyimpannya ke MongoDB. Tahapan:

---
1. Konfigurasi Web Scraping
- Menggunakan Selenium (dalam mode headless) untuk membuka halaman berita.
- Mendapatkan total halaman yang tersedia untuk discrape.

2. Mengambil Berita
- Menggunakan BeautifulSoup untuk mengekstrak elemen berita seperti judul, tanggal, isi, dan link.
- Mengabaikan elemen yang tidak relevan (iklan/zoom, dll).

3. Penyimpanan ke MongoDB
- Data berita disimpan dalam database bigdata_project.
- Duplikasi dicegah dengan memeriksa keberadaan judul sebelumnya.
