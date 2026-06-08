# DLH Kota Tasikmalaya Enterprise Flask

Website DLH Kota Tasikmalaya versi premium, modern, full stack, dan production-ready.

## Fitur

- Flask + SQLAlchemy
- Flask-Login authentication
- Flask-WTF CSRF protection
- Admin dashboard
- CMS layanan
- CMS berita
- CMS dokumen
- CMS galeri
- CMS link terkait
- Form kontak masuk database
- Form pengaduan masuk database
- Nomor tiket pengaduan
- Tracking pengaduan
- Search public dan API
- Pagination berita, dokumen, agenda, galeri
- SEO dasar
- robots.txt dan sitemap.xml
- Upload manager
- CSS modular per core dan per halaman
- Responsive 100%
- Siap Render, Railway, dan VPS Ubuntu

## Cara Menjalankan di Visual Studio Code

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Buka:

```text
http://localhost:5000
```

## Login Admin

```text
URL      : http://localhost:5000/admin/login
Username : admin
Password : admin123
```

## Struktur Penting

```text
app/
  models/
  routes/
  services/
  utils/
  templates/
    public/
    admin/
    errors/
  static/
    css/
      core/
      pages/
    js/
    img/
    uploads/
instance/
deploy/
migrations/
```

## Deploy Render

Gunakan:

```bash
gunicorn wsgi:app
```

Environment:

```text
SECRET_KEY=isi-dengan-secret-kuat
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@domain.com
ADMIN_PASSWORD=password-kuat
DATABASE_URL=sqlite:///instance/dlh_tasikmalaya.db
```

## Deploy VPS Ubuntu

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip nginx -y
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
gunicorn -w 3 -b 127.0.0.1:8000 wsgi:app
```

Gunakan Nginx reverse proxy dari folder `deploy/nginx`.

## Catatan Produksi

- Ganti `SECRET_KEY`.
- Ganti password admin default.
- Gunakan PostgreSQL untuk production skala besar.
- Simpan upload di storage persisten jika deploy di platform yang ephemeral.


## UPDATE FINAL SESUAI PERMINTAAN

- Warna topbar hijau sudah disamakan dengan screenshot.
- Database SQLite sudah dibuat dan dimasukkan ke folder `instance`.
- File database siap dibuka di VS Code melalui extension SQLite Viewer.
- Website sudah tersambung ke database melalui SQLAlchemy.
- Form kontak masuk ke tabel `contacts`.
- Form pengaduan masuk ke tabel `complaints`.
- Admin login membaca tabel `users`.
- CMS layanan, berita, dokumen, galeri, dan link membaca database.
