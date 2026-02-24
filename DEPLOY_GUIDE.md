# 🚀 Panduan Deploy Arunika ke Internet

Dokumen ini menjelaskan cara meng-online-kan website Flask Arunika agar bisa diakses siapapun di internet — dan ditemukan di Google.

---

## Pilih Platform Hosting

| Platform | Harga | Kemudahan | Cocok untuk |
|---|---|---|---|
| **Railway** ✅ *Rekomendasi* | Gratis s/d ~$5/bln | ⭐⭐⭐⭐⭐ Sangat mudah | Semua level |
| **Render** | Gratis (tidur 15 mnt) | ⭐⭐⭐⭐ Mudah | Testing / portofolio |
| **VPS (Hostinger/DigitalOcean)** | Rp 50–150 rb/bln | ⭐⭐⭐ Perlu sedikit teknis | Produksi serius |

**Rekomendasi: Railway** — deploy dalam 5 menit, tidak perlu kartu kredit untuk memulai, Flask langsung terdeteksi otomatis.

---

## OPSI A — Deploy ke Railway (Paling Mudah)

### Langkah 1: Siapkan File Tambahan di Folder Proyek

Buat 3 file berikut di dalam folder `techsite/`:

**`Procfile`** (tanpa ekstensi)
```
web: gunicorn app:app
```

**`runtime.txt`**
```
python-3.11.0
```

**`requirements.txt`** (perbarui isinya)
```
flask>=3.0
gunicorn>=21.0
```

### Langkah 2: Upload ke GitHub

1. Buat akun di [github.com](https://github.com) jika belum punya
2. Buat repository baru (klik **New** → beri nama `Arunika` → **Create repository**)
3. Upload semua file proyek:
   - Klik **uploading an existing file**
   - Seret seluruh isi folder `techsite/` ke sana
   - Klik **Commit changes**

### Langkah 3: Deploy di Railway

1. Buka [railway.app](https://railway.app) → **Login with GitHub**
2. Klik **New Project** → **Deploy from GitHub repo**
3. Pilih repository `Arunika`
4. Railway otomatis mendeteksi Flask — tunggu ~2 menit
5. Klik **Settings** → **Networking** → **Generate Domain**
6. Website Anda sekarang online di alamat seperti: `Arunika-production.up.railway.app`

**Selesai!** Website sudah bisa diakses siapapun.

---

## OPSI B — Deploy ke Render (Gratis Penuh)

> ⚠️ Kelemahan: server "tidur" setelah 15 menit tidak ada pengunjung, butuh 30 detik untuk "bangun" kembali. Cocok untuk portofolio atau testing.

### Langkah 1: Siapkan File Tambahan

Sama seperti Opsi A — buat `Procfile`, `runtime.txt`, dan perbarui `requirements.txt`.

### Langkah 2: Upload ke GitHub

Sama seperti Opsi A.

### Langkah 3: Deploy di Render

1. Buka [render.com](https://render.com) → **Sign Up with GitHub**
2. Klik **New** → **Web Service**
3. Pilih repository `Arunika`
4. Isi pengaturan:
   - **Name:** `Arunika`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Klik **Create Web Service**
6. Tunggu deploy selesai (~3–5 menit)
7. Website online di: `Arunika.onrender.com`

---

## OPSI C — VPS Hostinger (Paling Profesional, ~Rp 70rb/bln)

Cocok jika ingin kontrol penuh, performa stabil, dan domain sendiri.

### Langkah 1: Beli VPS

1. Buka [hostinger.com](https://hostinger.com) → pilih **KVM 1** (~Rp 70.000/bulan)
2. Pilih OS: **Ubuntu 22.04**
3. Catat **IP Address** dan **password root** dari email konfirmasi

### Langkah 2: Koneksi ke Server

Buka terminal (Mac/Linux) atau PowerShell (Windows):
```bash
ssh root@IP_ADDRESS_ANDA
```

### Langkah 3: Instalasi di Server

```bash
# Update sistem
apt update && apt upgrade -y

# Install Python dan Nginx
apt install python3-pip python3-venv nginx -y

# Buat folder proyek
mkdir /var/www/Arunika && cd /var/www/Arunika

# Upload file (dari komputer lokal, jalankan ini di terminal lokal):
# scp -r /path/ke/techsite/* root@IP_ADDRESS:/var/www/Arunika/
```

### Langkah 4: Setup Virtual Environment

```bash
cd /var/www/Arunika
python3 -m venv venv
source venv/bin/activate
pip install flask gunicorn
```

### Langkah 5: Konfigurasi Gunicorn

Buat file `/etc/systemd/system/Arunika.service`:
```ini
[Unit]
Description=Arunika Flask App
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/Arunika
Environment="PATH=/var/www/Arunika/venv/bin"
ExecStart=/var/www/Arunika/venv/bin/gunicorn --workers 2 --bind unix:Arunika.sock app:app

[Install]
WantedBy=multi-user.target
```

```bash
systemctl start Arunika
systemctl enable Arunika
```

### Langkah 6: Konfigurasi Nginx

Buat file `/etc/nginx/sites-available/Arunika`:
```nginx
server {
    listen 80;
    server_name Arunika.com www.Arunika.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/Arunika/Arunika.sock;
    }

    location /static {
        alias /var/www/Arunika/static;
    }
}
```

```bash
ln -s /etc/nginx/sites-available/Arunika /etc/nginx/sites-enabled
nginx -t && systemctl restart nginx
```

---

## Menghubungkan Domain Sendiri

Setelah website online di Railway/Render/VPS, hubungkan domain kustom:

### Beli Domain (jika belum punya)

Rekomendasi provider domain Indonesia:
- **Niagahoster** — [niagahoster.co.id](https://niagahoster.co.id) (~Rp 150rb/tahun untuk .com)
- **IDwebhost** — [idwebhost.com](https://idwebhost.com)
- **Namecheap** — [namecheap.com](https://namecheap.com) (lebih murah, bayar USD)

### Setting DNS

Di panel domain Anda, buat record DNS:

**Jika pakai Railway/Render:**
```
Type: CNAME
Name: www
Value: [alamat yang diberikan Railway/Render]
TTL: Auto

Type: CNAME  
Name: @
Value: [alamat yang diberikan Railway/Render]
TTL: Auto
```

**Jika pakai VPS:**
```
Type: A
Name: @
Value: [IP Address VPS Anda]
TTL: Auto

Type: A
Name: www
Value: [IP Address VPS Anda]
TTL: Auto
```

Tunggu propagasi DNS: biasanya 5–30 menit, maksimal 24 jam.

### Aktifkan HTTPS (SSL Gratis)

**Railway/Render:** SSL otomatis aktif begitu domain terhubung.

**VPS (Let's Encrypt):**
```bash
apt install certbot python3-certbot-nginx -y
certbot --nginx -d Arunika.com -d www.Arunika.com
# Ikuti instruksi, masukkan email, setujui Terms
```

SSL akan otomatis diperbarui setiap 90 hari.

---

## Agar Website Muncul di Google (SEO Dasar)

Setelah website online, lakukan ini agar Google mulai mengindeks:

### 1. Daftarkan ke Google Search Console

1. Buka [search.google.com/search-console](https://search.google.com/search-console)
2. Klik **Add Property** → masukkan URL website Anda
3. Verifikasi kepemilikan (pilih metode HTML tag — salin kode meta ke `base.html` di dalam `<head>`)
4. Submit **Sitemap** (tambahkan `/sitemap.xml` — lihat langkah berikutnya)

### 2. Tambahkan Sitemap

Tambahkan route ini di `app.py`:

```python
from flask import Response

@app.route("/sitemap.xml")
def sitemap():
    base = "https://Arunika.com"  # ganti dengan domain Anda
    pages = [
        ("", "weekly", "1.0"),
        ("/services", "monthly", "0.9"),
        ("/services/web-development", "monthly", "0.9"),
        ("/services/ai-solutions", "monthly", "0.9"),
        ("/why-us", "monthly", "0.8"),
        ("/portfolio", "monthly", "0.8"),
        ("/faq", "monthly", "0.7"),
        ("/contact", "monthly", "0.6"),
    ]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, freq, prio in pages:
        xml.append(f"""  <url>
    <loc>{base}{path}</loc>
    <changefreq>{freq}</changefreq>
    <priority>{prio}</priority>
  </url>""")
    xml.append("</urlset>")
    return Response("\n".join(xml), mimetype="application/xml")
```

### 3. Tambahkan robots.txt

```python
@app.route("/robots.txt")
def robots():
    base = "https://Arunika.com"  # ganti dengan domain Anda
    content = f"""User-agent: *
Allow: /
Sitemap: {base}/sitemap.xml"""
    return Response(content, mimetype="text/plain")
```

### 4. Set SECRET_KEY yang Aman

Di Railway/Render, buka **Environment Variables** dan tambahkan:
```
SECRET_KEY = [string acak panjang, contoh: buat di https://djecrety.ir]
```

---

## Checklist Sebelum Live

- [ ] `Procfile` sudah dibuat
- [ ] `requirements.txt` sudah diperbarui (ada `gunicorn`)
- [ ] `SECRET_KEY` diset lewat environment variable, bukan hardcoded
- [ ] Website bisa dibuka dari browser dengan HTTPS
- [ ] Semua halaman bisa diakses (/, /services, /faq, /contact, dst.)
- [ ] Sitemap sudah didaftarkan ke Google Search Console
- [ ] `robots.txt` bisa diakses di `/robots.txt`
- [ ] Gambar (jika ada) memiliki atribut `alt`
- [ ] Judul dan meta description berbeda di tiap halaman (sudah ada di translations)

---

## Estimasi Waktu

| Langkah | Waktu |
|---|---|
| Siapkan file + upload GitHub | 15 menit |
| Deploy Railway/Render | 5–10 menit |
| Hubungkan domain | 30 menit + tunggu propagasi DNS |
| Daftar Google Search Console | 10 menit |
| Google mulai mengindeks | 1–14 hari |

---

## Ringkasan Rekomendasi

**Mulai cepat & gratis:** Railway → sambungkan domain → daftar Search Console.

**Serius & jangka panjang:** VPS Hostinger (Rp 70rb/bln) + domain .com (Rp 150rb/tahun) = total sekitar **Rp 220rb/tahun** untuk website profesional yang selalu online.
