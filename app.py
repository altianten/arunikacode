import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, redirect, url_for, make_response, g, Response

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")

# ── Load translations ─────────────────────────────────────────────────────────
TRANSLATIONS = {}
SUPPORTED_LANGS = ["en", "id"]
DEFAULT_LANG = "en"

for lang in SUPPORTED_LANGS:
    path = os.path.join(app.root_path, "translations", f"{lang}.json")
    with open(path, encoding="utf-8") as f:
        TRANSLATIONS[lang] = json.load(f)


# ── Language middleware ───────────────────────────────────────────────────────
@app.before_request
def set_language():
    path = request.path.lstrip("/")
    prefix = path.split("/")[0] if path else ""
    if prefix in SUPPORTED_LANGS:
        g.lang = prefix
    else:
        g.lang = request.cookies.get("lang", DEFAULT_LANG)
        if g.lang not in SUPPORTED_LANGS:
            g.lang = DEFAULT_LANG


def t(key_path: str) -> str:
    keys = key_path.split(".")
    data = TRANSLATIONS.get(g.lang, TRANSLATIONS[DEFAULT_LANG])
    for k in keys:
        if isinstance(data, dict):
            data = data.get(k, key_path)
        else:
            return key_path
    return data


@app.context_processor
def inject_globals():
    return {
        "t": t,
        "lang": g.lang,
        "supported_langs": SUPPORTED_LANGS,
        "lang_names": {
            "en": TRANSLATIONS["en"]["lang_name"],
            "id": TRANSLATIONS["id"]["lang_name"],
        },
    }


# ── Language switcher ─────────────────────────────────────────────────────────
@app.route("/set-lang/<lang>")
def set_lang(lang):
    if lang not in SUPPORTED_LANGS:
        lang = DEFAULT_LANG
    referrer = request.referrer or "/"
    response = make_response(redirect(referrer))
    response.set_cookie("lang", lang, max_age=60 * 60 * 24 * 365, samesite="Lax")
    return response


# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def home():
    return render_template("home.html", page="home")


@app.route("/services")
def services():
    return render_template("services.html", page="services")


@app.route("/services/web-development")
def web_pricing():
    packages = [
        {"key": "pkg_portfolio",    "popular": False, "features": ["f1","f2","f3","f4","f5","f6"]},
        {"key": "pkg_umkm",         "popular": False, "features": ["f1","f2","f3","f4","f5","f6","f7"]},
        {"key": "pkg_basic",        "popular": True,  "features": ["f1","f2","f3","f4","f5","f6"]},
        {"key": "pkg_professional", "popular": False, "features": ["f1","f2","f3","f4","f5","f6","f7","f8"]},
    ]
    return render_template("web_pricing.html", page="services", packages=packages)


@app.route("/services/ai-solutions")
def ai_pricing():
    packages = [
        {"key": "pkg_chatbot",   "popular": True,  "features": ["f1","f2","f3","f4","f5","f6"]},
        {"key": "pkg_cleaning",  "popular": False, "features": ["f1","f2","f3","f4","f5","f6"]},
        {"key": "pkg_eda",       "popular": False, "features": ["f1","f2","f3","f4","f5","f6"]},
        {"key": "pkg_ml",        "popular": False, "features": ["f1","f2","f3","f4","f5","f6"]},
        {"key": "pkg_dashboard", "popular": False, "features": ["f1","f2","f3","f4","f5","f6"]},
    ]
    return render_template("ai_pricing.html", page="services", packages=packages)


@app.route("/why-us")
def why_us():
    return render_template("why_us.html", page="why_us")


@app.route("/portfolio")
def portfolio():
    projects = [
        {"key": "project_1", "tag": "web",  "slug": "edutrack"},
        {"key": "project_2", "tag": "ai",   "slug": "retailbot"},
        {"key": "project_3", "tag": "web",  "slug": "arunika-portfolio"},
        {"key": "project_4", "tag": "web",  "slug": "tingkir-lor"},
        {"key": "project_5", "tag": "ai",   "slug": "salesvision"},
        {"key": "project_6", "tag": "ai",   "slug": "studentdrop"},
        {"key": "project_7", "tag": "ai",   "slug": "marketpulse"},
    ]
    return render_template("portfolio.html", page="portfolio", projects=projects)


CASE_STUDIES = {
    "edutrack": {
        "title":   {"en": "EduTrack Dashboard",   "id": "EduTrack Dashboard"},
        "category":{"en": "Web Development",       "id": "Web Development"},
        "summary": {
            "en": "A student performance tracking dashboard built for a local university — helping lecturers identify at-risk students early and act fast.",
            "id": "Dashboard pemantauan performa mahasiswa untuk universitas lokal — membantu dosen mendeteksi mahasiswa yang berisiko sejak dini dan mengambil tindakan cepat.",
        },
        "stats": [
            {"value": "40%",  "label": {"en": "Faster reporting",  "id": "Pelaporan lebih cepat"}},
            {"value": "300+", "label": {"en": "Students tracked",   "id": "Mahasiswa terpantau"}},
            {"value": "2wks", "label": {"en": "Delivery time",      "id": "Waktu pengerjaan"}},
        ],
        "challenge": {
            "en": "Lecturers at a local university were manually tracking student grades across spreadsheets, making it slow and error-prone to identify struggling students until it was too late. They needed a centralized, visual system that could surface at-risk students instantly.",
            "id": "Dosen di sebuah universitas lokal memantau nilai mahasiswa secara manual lewat spreadsheet — lambat, rawan kesalahan, dan mahasiswa yang kesulitan baru terdeteksi saat sudah terlambat. Mereka butuh sistem terpusat dan visual yang bisa menampilkan mahasiswa berisiko secara langsung.",
        },
        "solution": {
            "en": "We built a Flask-based web dashboard connected to the university's existing data exports. The system visualizes grade trends, attendance, and assignment completion in real time — with automatic flagging for students falling below thresholds.",
            "id": "Kami membangun dashboard web berbasis Flask yang terhubung dengan ekspor data universitas yang sudah ada. Sistem ini memvisualisasikan tren nilai, kehadiran, dan penyelesaian tugas secara real-time — dengan penanda otomatis untuk mahasiswa yang nilainya di bawah ambang batas.",
        },
        "solution_points": {
            "en": ["Automated import from existing Excel/CSV grade sheets", "Visual grade trend charts per student using Chart.js", "At-risk student flagging with color-coded alerts", "Filter by class, semester, and subject", "Exportable PDF reports for department heads"],
            "id": ["Import otomatis dari file Excel/CSV nilai yang sudah ada", "Grafik tren nilai per mahasiswa menggunakan Chart.js", "Penanda mahasiswa berisiko dengan kode warna", "Filter berdasarkan kelas, semester, dan mata kuliah", "Laporan PDF yang bisa diekspor untuk kepala jurusan"],
        },
        "tech": ["Python", "Flask", "Chart.js", "SQLite", "Tailwind CSS", "Pandas"],
        "result": {
            "en": "The dashboard reduced the time lecturers spent generating reports by 40%. At-risk students are now identified in real time instead of at the end of semester, allowing for earlier intervention and better student outcomes.",
            "id": "Dashboard ini mengurangi waktu yang dihabiskan dosen untuk membuat laporan sebesar 40%. Mahasiswa berisiko kini teridentifikasi secara real-time, bukan di akhir semester, sehingga intervensi bisa dilakukan lebih awal dan hasil belajar mahasiswa meningkat.",
        },
    },
    "retailbot": {
        "title":   {"en": "RetailBot AI",  "id": "RetailBot AI"},
        "category":{"en": "AI Solutions",  "id": "Solusi AI"},
        "summary": {
            "en": "A WhatsApp-integrated AI chatbot for an SME clothing brand — handling customer FAQs, order tracking, and product recommendations around the clock.",
            "id": "Chatbot AI terintegrasi WhatsApp untuk brand fashion UMKM — menangani FAQ pelanggan, pelacakan pesanan, dan rekomendasi produk sepanjang waktu.",
        },
        "stats": [
            {"value": "60%",    "label": {"en": "Fewer support tickets", "id": "Tiket dukungan berkurang"}},
            {"value": "24/7",   "label": {"en": "Availability",           "id": "Tersedia"}},
            {"value": "3 hari", "label": {"en": "Deployment time",        "id": "Waktu deployment"}},
        ],
        "challenge": {
            "en": "A growing SME clothing brand was overwhelmed with repetitive WhatsApp messages from customers asking about sizes, stock availability, and order status. The owner was spending 3–4 hours daily just answering these messages — time that could be spent running the business.",
            "id": "Brand fashion UMKM yang sedang berkembang kewalahan dengan pesan WhatsApp berulang dari pelanggan yang menanyakan ukuran, ketersediaan stok, dan status pesanan. Pemilik menghabiskan 3–4 jam sehari hanya untuk membalas pesan — waktu yang seharusnya bisa digunakan untuk menjalankan bisnis.",
        },
        "solution": {
            "en": "We built a custom AI chatbot integrated directly into their WhatsApp Business account. The bot was trained on their product catalog, FAQ, and order workflow — and escalates complex questions to the human owner only when needed.",
            "id": "Kami membangun chatbot AI khusus yang terintegrasi langsung ke akun WhatsApp Business mereka. Bot ini dilatih menggunakan katalog produk, FAQ, dan alur pemesanan — dan hanya meneruskan pertanyaan kompleks ke pemilik saat diperlukan.",
        },
        "solution_points": {
            "en": ["WhatsApp Business API integration", "Custom-trained on product catalog and FAQ", "Automated order status lookup", "Product recommendation based on customer preferences", "Seamless handoff to human agent when needed", "Conversation history logging for business insights"],
            "id": ["Integrasi WhatsApp Business API", "Dilatih khusus menggunakan katalog produk dan FAQ", "Pencarian status pesanan otomatis", "Rekomendasi produk berdasarkan preferensi pelanggan", "Penerusan mulus ke agen manusia saat diperlukan", "Pencatatan riwayat percakapan untuk insight bisnis"],
        },
        "tech": ["Python", "LLM API", "WhatsApp Business API", "Flask", "SQLite"],
        "result": {
            "en": "Support ticket volume dropped by 60% in the first two weeks. The owner reclaimed over 3 hours daily, response times went from hours to seconds, and customer satisfaction improved noticeably due to instant, accurate replies.",
            "id": "Volume tiket dukungan turun 60% dalam dua minggu pertama. Pemilik mendapatkan kembali lebih dari 3 jam sehari, waktu respons dari berjam-jam menjadi hitungan detik, dan kepuasan pelanggan meningkat signifikan berkat balasan yang cepat dan akurat.",
        },
    },
    "arunika-portfolio": {
        "title":   {"en": "Arunika Portfolio",  "id": "Portofolio Arunika"},
        "category":{"en": "Web Development",    "id": "Web Development"},
        "summary": {
            "en": "A sleek personal portfolio site for a fresh computer science graduate — showcasing projects, skills, and contact in one clean, fast-loading page.",
            "id": "Website portofolio personal yang bersih dan profesional untuk fresh graduate teknologi — menampilkan proyek, keahlian, dan kontak dalam satu halaman yang cepat dan rapi.",
        },
        "stats": [
            {"value": "3",    "label": {"en": "Freelance clients landed", "id": "Klien freelance didapat"}},
            {"value": "1mgg", "label": {"en": "Delivery time",            "id": "Waktu pengerjaan"}},
            {"value": "100%", "label": {"en": "Mobile responsive",        "id": "Responsif di semua perangkat"}},
        ],
        "challenge": {
            "en": "A fresh computer science graduate needed an online presence fast — something that looked professional, loaded quickly, and stood out enough to attract freelance clients. They had no prior website and a limited budget.",
            "id": "Seorang fresh graduate teknologi membutuhkan kehadiran online dengan cepat — sesuatu yang terlihat profesional, cepat dimuat, dan cukup menonjol untuk menarik klien freelance. Mereka belum punya website dan punya anggaran terbatas.",
        },
        "solution": {
            "en": "We designed and developed a single-page portfolio site with a focus on performance, clean aesthetics, and strong calls-to-action. The site highlights their projects, tech skills, and contact info in a way that's easy for non-technical clients to navigate.",
            "id": "Kami merancang dan mengembangkan website portofolio satu halaman dengan fokus pada performa, estetika yang bersih, dan call-to-action yang kuat. Website ini menonjolkan proyek, keahlian teknis, dan informasi kontak secara mudah dipahami oleh klien non-teknis.",
        },
        "solution_points": {
            "en": ["Single-page layout optimized for fast load times", "Project showcase with live demo and GitHub links", "Skills section with visual proficiency indicators", "Contact form with direct email integration", "SEO-ready structure for Google discoverability", "Dark mode support out of the box"],
            "id": ["Tata letak satu halaman yang dioptimalkan untuk loading cepat", "Tampilan proyek dengan tautan demo langsung dan GitHub", "Bagian keahlian dengan indikator visual", "Formulir kontak dengan integrasi email langsung", "Struktur siap SEO untuk ditemukan di Google", "Dukungan mode gelap bawaan"],
        },
        "tech": ["HTML", "CSS", "JavaScript", "Flask", "Tailwind CSS"],
        "result": {
            "en": "Within a month of launch, the client landed 3 freelance projects directly through the website contact form. The portfolio became their primary tool for pitching to potential clients and applying for jobs.",
            "id": "Dalam sebulan sejak diluncurkan, klien berhasil mendapatkan 3 proyek freelance langsung melalui formulir kontak website. Portofolio ini menjadi alat utama mereka untuk mempresentasikan diri ke calon klien dan melamar pekerjaan.",
        },
    },
    "tingkir-lor": {
        "title":   {"en": "Tingkir Lor Village Tourism Website", "id": "Website Desa Wisata Tingkir Lor"},
        "category":{"en": "Web Development", "id": "Web Development"},
        "summary": {
            "en": "A digital platform for Desa Wisata Tingkir Lor, Salatiga — bringing the village's clothing fabric industry, scenic spots, Javanese culture, and religious tourism to the internet for the first time.",
            "id": "Platform digital untuk Desa Wisata Tingkir Lor, Salatiga — menghadirkan industri kain pakaian lokal, wisata alam, budaya Jawa, dan wisata religi desa ini ke internet untuk pertama kalinya.",
        },
        "stats": [
            {"value": "1st",  "label": {"en": "Digital presence",  "id": "Kehadiran digital perdana"}},
            {"value": "4+",   "label": {"en": "UMKM featured",     "id": "UMKM ditampilkan"}},
            {"value": "3mgg", "label": {"en": "Delivery time",     "id": "Waktu pengerjaan"}},
        ],
        "challenge": {
            "en": "Desa Wisata Tingkir Lor in Salatiga had significant tourism and economic potential — local SMEs producing fabric for clothing (shorts, casual wear, and similar garments), scenic natural views, rich Javanese cultural traditions, and important religious sites. But without any digital presence, the village was invisible to visitors and buyers outside the area. Word of mouth was the only way people found out about it.",
            "id": "Desa Wisata Tingkir Lor di Salatiga memiliki potensi wisata dan ekonomi yang besar — UMKM lokal yang memproduksi kain untuk pakaian (celana kolor, pakaian kasual, dan sejenisnya), pemandangan alam yang indah, tradisi budaya Jawa yang kaya, serta situs-situs religi penting. Namun tanpa kehadiran digital sama sekali, desa ini tidak terlihat oleh wisatawan maupun pembeli dari luar daerah. Satu-satunya cara orang mengetahuinya hanyalah dari mulut ke mulut.",
        },
        "solution": {
            "en": "We built a comprehensive village tourism website that serves as the digital front door for Tingkir Lor. The site presents the village's tourism offerings in a clear, attractive format — covering UMKM products, natural attractions, cultural events, and religious sites.",
            "id": "Kami membangun website wisata desa yang komprehensif sebagai pintu masuk digital bagi Tingkir Lor. Website ini menampilkan semua potensi wisata desa secara menarik dan terstruktur — mulai dari produk UMKM, objek wisata alam, agenda budaya, hingga situs religi.",
        },
        "solution_points": {
            "en": ["Village profile and history page", "UMKM directory with product photos and contact info", "Interactive map of tourism spots", "Cultural events calendar", "Religious tourism guide (mosque, pesantren, pilgrimage sites)", "Gallery of village scenery and activities", "Contact and visit planning section"],
            "id": ["Halaman profil dan sejarah desa", "Direktori UMKM lengkap dengan foto produk dan info kontak", "Peta interaktif objek wisata", "Kalender agenda budaya dan acara desa", "Panduan wisata religi (masjid, pesantren, situs ziarah)", "Galeri foto pemandangan dan kegiatan desa", "Informasi kontak dan perencanaan kunjungan"],
        },
        "tech": ["Python", "Flask", "Tailwind CSS", "Leaflet.js", "SQLite"],
        "result": {
            "en": "Tingkir Lor now has a professional digital presence that reaches visitors across Indonesia. Local UMKM are now discoverable online, tourism spots are clearly mapped, and the village has a platform to promote cultural events and attract new visitors.",
            "id": "Tingkir Lor kini memiliki kehadiran digital yang profesional dan bisa dijangkau wisatawan dari seluruh Indonesia. UMKM lokal kini bisa ditemukan secara online, objek wisata terpetakan dengan jelas, dan desa punya platform untuk mempromosikan agenda budaya serta menarik wisatawan baru.",
        },
    },
    "salesvision": {
        "title":   {"en": "SalesVision Dashboard",  "id": "SalesVision Dashboard"},
        "category":{"en": "AI / Dashboard",          "id": "AI / Dashboard"},
        "summary": {
            "en": "An interactive sales & revenue dashboard for an FMCG distributor — turning raw transaction data into real-time business intelligence with automated monthly reports.",
            "id": "Dashboard penjualan interaktif untuk distributor FMCG — mengubah data transaksi mentah menjadi business intelligence real-time dengan laporan bulanan otomatis.",
        },
        "stats": [
            {"value": "50%",  "label": {"en": "Faster decisions",    "id": "Keputusan lebih cepat"}},
            {"value": "12+",  "label": {"en": "KPI metrics tracked", "id": "KPI terpantau"}},
            {"value": "2mgg", "label": {"en": "Delivery time",       "id": "Waktu pengerjaan"}},
        ],
        "challenge": {
            "en": "An FMCG distributor with hundreds of daily transactions was still relying on manual Excel reports to track sales performance. Reports took days to compile, were often outdated by the time they reached management, and provided no way to drill down into specific products, regions, or time periods.",
            "id": "Distributor FMCG dengan ratusan transaksi harian masih mengandalkan laporan Excel manual. Laporan membutuhkan berhari-hari untuk dikompilasi, sering sudah usang saat sampai ke manajemen, dan tidak bisa di-drill down ke produk, wilayah, atau periode tertentu.",
        },
        "solution": {
            "en": "We built an interactive dashboard connected to their transaction database, visualizing sales data in real time. Management can now filter by product, region, salesperson, and date range — and receive automated PDF reports every month.",
            "id": "Kami membangun dashboard interaktif yang terhubung ke database transaksi mereka secara real-time. Manajemen kini bisa filter berdasarkan produk, wilayah, salesperson, dan rentang tanggal — serta menerima laporan PDF otomatis setiap bulan.",
        },
        "solution_points": {
            "en": ["Real-time sales & revenue visualization", "12+ KPI cards (revenue, margin, growth, top products)", "Filter by product, region, salesperson, date range", "Trend charts with month-over-month comparison", "Automated monthly PDF report via email", "Mobile-responsive for on-the-go access"],
            "id": ["Visualisasi penjualan & pendapatan real-time", "12+ KPI card (revenue, margin, pertumbuhan, produk terlaris)", "Filter berdasarkan produk, wilayah, salesperson, rentang tanggal", "Grafik tren dengan perbandingan bulan ke bulan", "Laporan PDF bulanan otomatis via email", "Responsif di mobile untuk akses kapan saja"],
        },
        "tech": ["Python", "Pandas", "Plotly", "Flask", "SQLite", "WeasyPrint"],
        "result": {
            "en": "Management can now make data-driven decisions in minutes instead of days. The dashboard reduced report preparation time by 50% and surfaced insights that led to a 15% improvement in top-selling product allocation.",
            "id": "Manajemen kini bisa mengambil keputusan berbasis data dalam menit, bukan hari. Dashboard mengurangi waktu persiapan laporan 50% dan mengungkap insight yang berujung pada peningkatan 15% alokasi produk terlaris.",
        },
    },
    "studentdrop": {
        "title":   {"en": "StudentDrop ML Model",   "id": "StudentDrop ML Model"},
        "category":{"en": "AI / Machine Learning",   "id": "AI / Machine Learning"},
        "summary": {
            "en": "A machine learning model predicting student dropout risk for a vocational school — trained on attendance, grades, and socioeconomic data to enable early intervention.",
            "id": "Model machine learning untuk memprediksi risiko dropout siswa di SMK — dilatih dari data kehadiran, nilai, dan sosial ekonomi untuk memungkinkan intervensi lebih awal.",
        },
        "stats": [
            {"value": "87%",  "label": {"en": "Prediction accuracy", "id": "Akurasi prediksi"}},
            {"value": "200+", "label": {"en": "Students analyzed",   "id": "Siswa dianalisis"}},
            {"value": "3mgg", "label": {"en": "Delivery time",       "id": "Waktu pengerjaan"}},
        ],
        "challenge": {
            "en": "A vocational school was struggling with a high dropout rate but had no way to identify at-risk students before it was too late. Counselors were reactive — only finding out about problems when students had already stopped attending.",
            "id": "Sebuah SMK menghadapi tingkat dropout yang tinggi namun tidak memiliki cara untuk mengidentifikasi siswa berisiko sebelum terlambat. Konselor bersifat reaktif — baru mengetahui masalah saat siswa sudah berhenti hadir.",
        },
        "solution": {
            "en": "We developed a machine learning classification model trained on 3 years of historical student data. The model scores each student's dropout risk weekly and flags high-risk students for counselor follow-up — before they actually drop out.",
            "id": "Kami mengembangkan model klasifikasi machine learning yang dilatih dari 3 tahun data historis siswa. Model menilai risiko dropout setiap siswa mingguan dan menandai siswa berisiko tinggi untuk ditindaklanjuti konselor — sebelum mereka benar-benar keluar.",
        },
        "solution_points": {
            "en": ["Data preprocessing from attendance, grades & socioeconomic records", "Feature engineering (trend analysis, rolling averages)", "Classification model with 87% accuracy", "Weekly risk scoring dashboard for counselors", "Automated alert system for high-risk students", "Model performance monitoring & retraining pipeline"],
            "id": ["Preprocessing data dari catatan kehadiran, nilai & sosial ekonomi", "Feature engineering (analisis tren, rolling average)", "Model klasifikasi dengan akurasi 87%", "Dashboard skor risiko mingguan untuk konselor", "Sistem peringatan otomatis untuk siswa berisiko tinggi", "Monitoring performa model & pipeline retraining"],
        },
        "tech": ["Python", "Scikit-learn", "Pandas", "XGBoost", "Flask", "Chart.js"],
        "result": {
            "en": "The school identified 34 high-risk students in the first month. Early interventions successfully retained 28 of them. Dropout rate dropped by 18% in the following semester.",
            "id": "Sekolah mengidentifikasi 34 siswa berisiko tinggi di bulan pertama. Intervensi awal berhasil mempertahankan 28 di antaranya. Tingkat dropout turun 18% di semester berikutnya.",
        },
    },
    "marketpulse": {
        "title":   {"en": "MarketPulse EDA",        "id": "MarketPulse EDA"},
        "category":{"en": "AI / Data Analysis",      "id": "AI / Analisis Data"},
        "summary": {
            "en": "An exploratory data analysis project for an online marketplace SME — uncovering buying patterns, peak hours, and top categories to sharpen their marketing strategy.",
            "id": "Proyek analisis data eksploratif untuk UMKM marketplace online — mengungkap pola pembelian, jam sibuk, dan kategori terlaris untuk menajamkan strategi pemasaran mereka.",
        },
        "stats": [
            {"value": "3",    "label": {"en": "Key growth insights",   "id": "Insight pertumbuhan"}},
            {"value": "50K+", "label": {"en": "Transactions analyzed", "id": "Transaksi dianalisis"}},
            {"value": "1mgg", "label": {"en": "Delivery time",         "id": "Waktu pengerjaan"}},
        ],
        "challenge": {
            "en": "An SME running an online marketplace had 2 years of transaction data sitting unused in spreadsheets. They had a gut feeling about which products performed best — but no data to back it up or guide their promotional spending.",
            "id": "UMKM yang menjalankan marketplace online memiliki 2 tahun data transaksi yang tidak terpakai di spreadsheet. Mereka punya intuisi tentang produk terbaik — tapi tidak ada data untuk membuktikannya atau mengarahkan anggaran promosi.",
        },
        "solution": {
            "en": "We conducted a comprehensive EDA on 50,000+ transactions — cleaning the data, identifying patterns, and delivering a clear slide deck with actionable recommendations.",
            "id": "Kami melakukan EDA komprehensif pada 50.000+ transaksi — membersihkan data, mengidentifikasi pola, dan menyajikan slide deck yang jelas dengan rekomendasi actionable.",
        },
        "solution_points": {
            "en": ["Data cleaning & normalization of 50K+ records", "Time-series analysis by hour, day, and month", "Product category performance ranking", "Customer segmentation by frequency & value", "Correlation analysis between promotions and sales spikes", "Final report with 3 prioritized growth recommendations"],
            "id": ["Pembersihan & normalisasi 50K+ catatan transaksi", "Analisis time-series per jam, hari, dan bulan", "Peringkat performa kategori produk", "Segmentasi pelanggan berdasarkan frekuensi & nilai", "Analisis korelasi antara promosi dan lonjakan penjualan", "Laporan akhir dengan 3 rekomendasi pertumbuhan"],
        },
        "tech": ["Python", "Pandas", "Matplotlib", "Seaborn", "Jupyter Notebook", "PowerPoint"],
        "result": {
            "en": "Analysis revealed 3 high-impact insights: peak buying hours (7–9 PM), an underperforming category draining ad budget, and a loyal customer segment not targeted with retention offers. The client improved ROI by 22% the following quarter.",
            "id": "Analisis mengungkap 3 insight: jam puncak pembelian (19–21), kategori yang menguras anggaran iklan, dan segmen pelanggan setia yang belum ditarget. Klien meningkatkan ROI 22% di kuartal berikutnya.",
        },
    },
}


@app.route("/portfolio/<slug>")
def case_study(slug):
    project_raw = CASE_STUDIES.get(slug)
    if not project_raw:
        return redirect(url_for("portfolio"))
    lang = g.lang

    # Resolve bilingual fields
    def r(field):
        val = project_raw.get(field, "")
        return val.get(lang, val.get("en", "")) if isinstance(val, dict) else val

    project = {
        "title":    r("title"),
        "category": r("category"),
        "summary":  r("summary"),
        "challenge":r("challenge"),
        "solution": r("solution"),
        "result":   r("result"),
        "tech":     project_raw["tech"],
        "stats": [
            {"value": s["value"], "label": s["label"].get(lang, s["label"].get("en", "")) if isinstance(s["label"], dict) else s["label"]}
            for s in project_raw["stats"]
        ],
        "solution_points": project_raw["solution_points"].get(lang, project_raw["solution_points"].get("en", [])) if isinstance(project_raw["solution_points"], dict) else project_raw["solution_points"],
        "slug": slug,
        "slug_to_key": {
            "edutrack":         "project_1",
            "retailbot":        "project_2",
            "arunika-portfolio":"project_3",
            "tingkir-lor":      "project_4",
            "salesvision":      "project_5",
            "studentdrop":      "project_6",
            "marketpulse":      "project_7",
        }.get(slug, ""),
    }
    return render_template("case_study.html", page="portfolio", project=project)


@app.route("/faq")
def faq():
    return render_template("faq.html", page="faq")


# ── Email config ──────────────────────────────────────────────────────────────
GMAIL_USER     = os.environ.get("GMAIL_USER", "altianten@gmail.com")
GMAIL_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")
NOTIFY_EMAIL   = os.environ.get("NOTIFY_EMAIL", "altianten@gmail.com")


def send_email(name, email, service, message):
    """Send contact form submission via Gmail SMTP."""
    if not GMAIL_PASSWORD:
        return False  # skip in dev if not configured

    subject = f"[Arunika] Pesan baru dari {name}"
    body = f"""Pesan baru masuk dari website Arunika!

Nama    : {name}
Email   : {email}
Layanan : {service or '-'}

Pesan:
{message}

---
Balas langsung ke: {email}
"""
    try:
        msg = MIMEMultipart()
        msg["From"]    = GMAIL_USER
        msg["To"]      = NOTIFY_EMAIL
        msg["Subject"] = subject
        msg["Reply-To"] = email
        msg.attach(MIMEText(body, "plain", "utf-8"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.sendmail(GMAIL_USER, NOTIFY_EMAIL, msg.as_string())
        return True
    except Exception:
        return False


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form_data = {}
    errors    = {}
    success   = False

    # Pre-fill from query params (from pricing pages)
    PACKAGE_NAMES = {
        # Web packages
        "pkg_portfolio":    {"en": "Web Portfolio Package",      "id": "Paket Web Portfolio"},
        "pkg_umkm":         {"en": "UMKM / SME Website Package", "id": "Paket Website UMKM"},
        "pkg_basic":        {"en": "Basic Website Package",      "id": "Paket Basic Website"},
        "pkg_professional": {"en": "Professional Website Package","id": "Paket Professional Website"},
        # AI packages
        "pkg_chatbot":      {"en": "AI Chatbot Package",         "id": "Paket AI Chatbot"},
        "pkg_cleaning":     {"en": "Data Cleaning Package",      "id": "Paket Data Cleaning"},
        "pkg_eda":          {"en": "EDA Package",                "id": "Paket EDA"},
        "pkg_ml":           {"en": "ML Model Package",           "id": "Paket ML Model"},
        "pkg_dashboard":    {"en": "Dashboard & Reporting Package","id": "Paket Dashboard & Reporting"},
    }

    if request.method == "GET":
        svc = request.args.get("service", "")
        pkg = request.args.get("package", "")
        pkg_info = PACKAGE_NAMES.get(pkg, {})
        pkg_name = pkg_info.get(g.lang, pkg_info.get("en", ""))
        form_data = {
            "service": "Web Development" if svc == "web" else "AI Solutions" if svc == "ai" else "",
            "message": pkg_name,
        }

    if request.method == "POST":
        name    = request.form.get("name", "").strip()
        email   = request.form.get("email", "").strip()
        service = request.form.get("service", "").strip()
        message = request.form.get("message", "").strip()

        form_data = {"name": name, "email": email, "service": service, "message": message}

        if not name:
            errors["name"] = t("contact.error_required")
        if not email:
            errors["email"] = t("contact.error_required")
        elif "@" not in email or "." not in email.split("@")[-1]:
            errors["email"] = t("contact.error_email")
        if not message:
            errors["message"] = t("contact.error_required")

        if not errors:
            send_email(name, email, service, message)
            success   = True
            form_data = {}

    return render_template("contact.html", page="contact",
                           form_data=form_data, errors=errors, success=success)


# ── SEO routes ───────────────────────────────────────────────────────────────
@app.route("/sitemap.xml")
def sitemap():
    base = os.environ.get("SITE_URL", "https://arunikacode.my.id").rstrip("/")
    pages = [
        ("",                           "weekly",  "1.0"),
        ("/services",                  "monthly", "0.9"),
        ("/services/web-development",  "monthly", "0.9"),
        ("/services/ai-solutions",     "monthly", "0.9"),
        ("/why-us",                    "monthly", "0.8"),
        ("/portfolio",                 "monthly", "0.8"),
        ("/faq",                       "monthly", "0.7"),
        ("/contact",                   "monthly", "0.6"),
    ]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, freq, prio in pages:
        xml.append(f"  <url>\n    <loc>{base}{path}</loc>\n    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>\n  </url>")
    xml.append("</urlset>")
    return Response("\n".join(xml), mimetype="application/xml")


@app.route("/robots.txt")
def robots():
    base = os.environ.get("SITE_URL", "https://arunikacode.my.id").rstrip("/")
    content = f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml"
    return Response(content, mimetype="text/plain")


@app.route("/<lang>/")
def home_lang(lang):
    if lang not in SUPPORTED_LANGS:
        return redirect(url_for("home"))
    response = make_response(redirect(url_for("home")))
    response.set_cookie("lang", lang, max_age=60 * 60 * 24 * 365, samesite="Lax")
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
