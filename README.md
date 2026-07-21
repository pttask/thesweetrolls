# The Sweet Rolls - Flask Web App

Website penjualan (POV user) untuk brand **The Sweet Rolls**, dibuat dengan Flask + Bootstrap 5.
Tugas 11 Praktikum Sistem Multimedia.

## Fitur

- **Home** — hero section interaktif: klik thumbnail (Banana / Choco / Cheese) untuk mengganti
  judul, deskripsi, warna latar, dan foto produk **tanpa reload halaman** (vanilla JS).
- **About** — profil brand The Sweet Rolls.
- **Product** — daftar produk dalam bentuk carousel card.
- **Product Detail** — halaman detail tiap produk (`/product/<slug>`) dengan pilihan qty dan tombol Add to Cart.
- **Checkout** — form data pengiriman & pembayaran dengan **validasi server-side**, ringkasan
  pesanan yang bisa diubah qty-nya secara AJAX (tanpa reload), dan penyimpanan order ke database.
- **Contact** — info toko, jam buka, dan embed Google Maps.
- Data produk & order disimpan di **SQLite** (`sweetrolls.db`).

## Struktur Folder

```
sweetrolls/
├── app.py              # Aplikasi Flask utama & routing
├── schema.sql           # Skema database SQLite
├── seed.py               # Script untuk mengisi data produk awal
├── requirements.txt
├── static/
│   ├── css/style.css
│   ├── js/main.js
│   └── images/          # Foto produk
└── templates/
    ├── base.html
    ├── home.html
    ├── about.html
    ├── product.html
    ├── product_detail.html
    ├── checkout.html
    ├── order_success.html
    └── contact.html
```

## Cara Menjalankan (Lokal)

```bash
# 1. Buat virtual environment (opsional tapi disarankan)
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Buat & isi database (hanya perlu sekali, atau saat reset data)
python seed.py

# 4. Jalankan server
python app.py
```

Buka browser ke: **http://127.0.0.1:5000**

## Reset Database

Jika ingin mengembalikan data produk ke awal (menghapus semua order yang pernah masuk):

```bash
rm sweetrolls.db
python seed.py
```

## Deploy ke Railway (Gratis)

Project ini sudah disiapkan untuk deploy langsung ke Railway (`Procfile` + auto-seed database).

1. Push project ini ke GitHub (kalau belum, lihat bagian atas README ini).
2. Buka [railway.app](https://railway.app), login pakai akun GitHub.
3. Klik **New Project → Deploy from GitHub repo**, pilih repo project ini.
4. Railway akan otomatis mendeteksi project Python lewat `requirements.txt` dan
   menjalankan perintah di `Procfile` (`gunicorn app:app`). Tidak perlu setting
   build/start command manual.
5. Di tab **Variables**, tambahkan environment variable:
   - `SECRET_KEY` — isi dengan string acak (untuk keamanan session), misalnya
     hasil dari `python -c "import secrets; print(secrets.token_hex(32))"`
6. Setelah deploy selesai, buka tab **Settings → Networking → Generate Domain**
   untuk mendapatkan URL publik (format `xxxx.up.railway.app`).
7. Database SQLite (`sweetrolls.db`) akan **otomatis dibuat & diisi data produk**
   saat aplikasi pertama kali jalan (lihat bagian "Auto-seed" di bawah) — tidak
   perlu menjalankan `python seed.py` manual di server.

### Catatan tentang penyimpanan data di Railway

Selama container berjalan (belum di-redeploy/restart), semua order yang masuk
lewat Checkout akan tersimpan normal di `sweetrolls.db`. Namun karena ini
adalah filesystem container biasa (bukan volume permanen), data akan **reset
ke data awal setiap kali project di-redeploy** (misalnya saat push commit
baru). Untuk penyimpanan yang benar-benar permanen di semua kondisi, bisa
ditambahkan [Railway Volume](https://docs.railway.app/guides/volumes) yang
di-mount ke path database — tapi untuk kebutuhan tugas ini, perilaku default
sudah cukup karena aplikasi tetap berfungsi penuh (checkout, validasi, dsb)
selama container aktif.

### Auto-seed database

`app.py` akan otomatis memanggil `seed_database()` dari `seed.py` saat
`sweetrolls.db` belum ada di server — jadi platform hosting apa pun (Railway,
Render, dll) bisa langsung deploy tanpa langkah manual tambahan.

## Deploy ke Render (Alternatif)

1. Push project ini ke GitHub.
2. Buat Web Service baru di [render.com](https://render.com), hubungkan ke repo GitHub.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`
5. Tambahkan environment variable `SECRET_KEY` (sama seperti langkah Railway di atas).
6. Deploy — Render akan memberi URL publik otomatis. Database ter-seed otomatis
   saat pertama kali jalan (lihat "Auto-seed database" di atas).

## Catatan

- Ini adalah aplikasi **POV user** (bukan admin/dashboard), sesuai ketentuan tugas.
- `app.py` membaca `SECRET_KEY` dari environment variable; kalau tidak diset,
  fallback ke nilai default (aman untuk lokal, **wajib** diisi env var sendiri saat deploy).
- Nomor WhatsApp & alamat di halaman Contact masih contoh — sesuaikan dengan data asli.
