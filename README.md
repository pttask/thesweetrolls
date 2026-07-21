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

## Deploy ke Render (Gratis)

1. Push project ini ke GitHub.
2. Buat Web Service baru di [render.com](https://render.com), hubungkan ke repo GitHub.
3. Build Command: `pip install -r requirements.txt && python seed.py`
4. Start Command: `gunicorn app:app`
   (tambahkan `gunicorn` ke `requirements.txt` sebelum deploy)
5. Deploy — Render akan memberi URL publik otomatis.

## Catatan

- Ini adalah aplikasi **POV user** (bukan admin/dashboard), sesuai ketentuan tugas.
- Ganti `app.secret_key` di `app.py` dengan nilai rahasia sebelum deploy ke production.
- Nomor WhatsApp & alamat di halaman Contact masih contoh — sesuaikan dengan data asli.
