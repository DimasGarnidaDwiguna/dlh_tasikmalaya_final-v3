from pathlib import Path
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, current_app, Response
from app.extensions import db
from app.models.content import Service, News, Agenda, Document, Gallery, LinkItem, ContactMessage, Complaint
from app.services.search_service import search_all
from app.utils.helpers import generate_ticket_number, only_digits

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def home():
    services = Service.query.filter_by(is_active=True).limit(4).all()
    news_items = News.query.filter_by(is_published=True).order_by(News.created_at.desc()).limit(3).all()
    gallery_items = Gallery.query.filter_by(type="foto").limit(6).all()
    stats = {
        "services": Service.query.count(),
        "news": News.query.count(),
        "documents": Document.query.count(),
        "complaints": Complaint.query.count(),
    }
    return render_template("public/home.html", services=services, news_items=news_items, gallery_items=gallery_items, stats=stats)


@public_bp.route("/profil/<page>")
def profile(page):
    titles = {
        "tentang": "Tentang DLH Kota Tasikmalaya",
        "tugas": "Tugas Pokok dan Fungsi",
        "visi-misi": "Visi dan Misi",
        "struktur": "Struktur Organisasi",
    }
    title = titles.get(page)
    if not title:
        return render_template("errors/404.html"), 404
    return render_template("public/profile.html", title=title, page=page)


@public_bp.route("/bidang/<page>")
def field(page):
    titles = {
        "tata-lingkungan": "Bidang Tata Lingkungan",
        "pengendalian-pencemaran": "Bidang Pengendalian Pencemaran dan Penataan Hukum Lingkungan",
        "pengelolaan-sampah": "Bidang Pengelolaan Sampah",
    }
    title = titles.get(page)
    if not title:
        return render_template("errors/404.html"), 404
    return render_template("public/field.html", title=title, page=page)


@public_bp.route("/pelayanan/<slug>")
def service_detail(slug):
    service = Service.query.filter_by(slug=slug, is_active=True).first()
    if not service:
        return render_template("errors/404.html"), 404
    return render_template("public/service_detail.html", service=service)


@public_bp.route("/dokumen/<page>")
def documents(page):
    if page == "download":
        page_num = request.args.get("page", 1, type=int)
        docs = Document.query.order_by(Document.year.desc(), Document.id.desc()).paginate(page=page_num, per_page=8, error_out=False)
        return render_template("public/documents.html", title="Download File", page=page, docs=docs)

    titles = {
        "peraturan-walikota": "Peraturan Walikota",
        "sop-air-limbah": "SOP Instalasi Pengelolaan Air Limbah",
        "sop-emisi": "SOP Instalasi Pengendali Emisi",
    }
    title = titles.get(page)
    if not title:
        return render_template("errors/404.html"), 404
    return render_template("public/documents.html", title=title, page=page, docs=None)


@public_bp.route("/download/<filename>")
def download_document(filename):
    # Prevent path traversal and only serve documents registered in database.
    safe_filename = Path(filename).name
    if safe_filename != filename or any(part in filename for part in ["..", "/", "\\"]):
        return render_template("errors/404.html"), 404

    doc = Document.query.filter_by(filename=safe_filename).first()
    if not doc:
        return render_template("errors/404.html"), 404

    stored_filename = Path(doc.filename).name
    if stored_filename != doc.filename:
        return render_template("errors/404.html"), 404

    doc.downloads += 1
    db.session.commit()
    return send_from_directory(current_app.config["UPLOAD_ROOT"] / "documents", stored_filename, as_attachment=True)


@public_bp.route("/informasi/<page>")
def information(page):
    page_num = request.args.get("page", 1, type=int)
    if page == "berita":
        items = News.query.filter_by(is_published=True).order_by(News.created_at.desc()).paginate(page=page_num, per_page=6, error_out=False)
        return render_template("public/information.html", title="Berita dan Artikel", page=page, items=items)
    if page == "agenda":
        items = Agenda.query.order_by(Agenda.date.asc()).paginate(page=page_num, per_page=8, error_out=False)
        return render_template("public/information.html", title="Agenda Kegiatan", page=page, items=items)
    if page == "panduan-umk":
        return render_template("public/information.html", title="Panduan Perizinan Berusaha Untuk UMK Risiko Rendah dan Badan Usaha", page=page, items=None)
    return render_template("errors/404.html"), 404


@public_bp.route("/berita/<slug>")
def news_detail(slug):
    item = News.query.filter_by(slug=slug, is_published=True).first()
    if not item:
        return render_template("errors/404.html"), 404
    item.views += 1
    db.session.commit()
    return render_template("public/news_detail.html", item=item)


@public_bp.route("/galeri/<page>")
def gallery(page):
    if page not in ["foto", "video"]:
        return render_template("errors/404.html"), 404
    page_num = request.args.get("page", 1, type=int)
    items = Gallery.query.filter_by(type=page).order_by(Gallery.id.desc()).paginate(page=page_num, per_page=9, error_out=False)
    title = "Galeri Foto" if page == "foto" else "Galeri Video"
    return render_template("public/gallery.html", title=title, page=page, items=items)


@public_bp.route("/link")
def links():
    items = LinkItem.query.order_by(LinkItem.id.asc()).all()
    return render_template("public/links.html", items=items)


@public_bp.route("/kontak", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        message = ContactMessage(
            name=request.form.get("name", "").strip(),
            email=request.form.get("email", "").strip(),
            subject=request.form.get("subject", "").strip(),
            message=request.form.get("message", "").strip(),
        )
        db.session.add(message)
        db.session.commit()
        flash("Pesan berhasil dikirim dan tersimpan ke database.", "success")
        return redirect(url_for("public.contact"))
    return render_template("public/contact.html")


@public_bp.route("/pengaduan", methods=["GET", "POST"])
def complaint():
    allowed_categories = {"Sampah", "Pencemaran Air", "Pencemaran Udara", "Limbah", "Lainnya"}

    if request.method == "POST":
        phone = request.form.get("phone", "").strip()
        category = request.form.get("category", "").strip()

        if not only_digits(phone, 8, 15):
            flash("No. telepon wajib berisi angka dengan panjang 8 sampai 15 digit.", "danger")
            return redirect(url_for("public.complaint"))

        if category not in allowed_categories:
            flash("Kategori pengaduan tidak valid.", "danger")
            return redirect(url_for("public.complaint"))

        last = Complaint.query.order_by(Complaint.id.desc()).first()
        complaint_data = Complaint(
            ticket_number=generate_ticket_number(last.id if last else 0),
            name=request.form.get("name", "").strip(),
            email=request.form.get("email", "").strip(),
            phone=phone,
            category=category,
            location=request.form.get("location", "").strip(),
            message=request.form.get("message", "").strip(),
        )
        db.session.add(complaint_data)
        db.session.commit()
        flash(f"Pengaduan berhasil dikirim. Nomor tiket: {complaint_data.ticket_number}", "success")
        return redirect(url_for("public.complaint"))
    return render_template("public/complaint.html")


@public_bp.route("/tracking", methods=["GET", "POST"])
def tracking():
    complaint_item = None
    if request.method == "POST":
        ticket = request.form.get("ticket_number", "").strip()
        complaint_item = Complaint.query.filter_by(ticket_number=ticket).first()
        if not complaint_item:
            flash("Nomor tiket tidak ditemukan.", "danger")
    return render_template("public/tracking.html", complaint=complaint_item)


@public_bp.route("/search")
def search():
    keyword = request.args.get("q", "").strip()
    results = search_all(keyword) if keyword else None
    return render_template("public/search.html", keyword=keyword, results=results)


@public_bp.route("/robots.txt")
def robots():
    return Response("User-agent: *\nAllow: /\nSitemap: /sitemap.xml\n", mimetype="text/plain")


@public_bp.route("/sitemap.xml")
def sitemap():
    base_url = request.url_root.rstrip("/")
    urls = [
        "", "/profil/tentang", "/profil/tugas", "/profil/visi-misi", "/profil/struktur",
        "/bidang/tata-lingkungan", "/bidang/pengendalian-pencemaran", "/bidang/pengelolaan-sampah",
        "/dokumen/download", "/informasi/berita", "/informasi/agenda", "/galeri/foto", "/galeri/video",
        "/kontak", "/pengaduan", "/tracking"
    ]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in urls:
        xml.append(f"<url><loc>{base_url}{url}</loc></url>")
    xml.append("</urlset>")
    return Response("\n".join(xml), mimetype="application/xml")
