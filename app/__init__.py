import os
from pathlib import Path
from flask import Flask, request, redirect
from werkzeug.middleware.proxy_fix import ProxyFix
from config import Config
from app.extensions import db, login_manager, migrate, csrf
from app.models.user import User
from app.models.content import (
    Service, NewsCategory, News, Agenda, Document, Gallery, LinkItem,
    VisitorLog
)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    app.config["UPLOAD_ROOT"].mkdir(parents=True, exist_ok=True)
    for sub in ["news", "gallery", "documents", "logos"]:
        (app.config["UPLOAD_ROOT"] / sub).mkdir(parents=True, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from app.routes.public import public_bp
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.api import api_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.before_request
    def log_visitor():
        if request.endpoint and not request.endpoint.startswith("static") and request.method == "GET":
            try:
                db.session.add(VisitorLog(
                    path=request.path,
                    ip_address=request.headers.get("X-Forwarded-For", request.remote_addr),
                    user_agent=request.headers.get("User-Agent", "")[:255]
                ))
                db.session.commit()
            except Exception:
                db.session.rollback()


    @app.before_request
    def enforce_https():
        if app.config.get("FORCE_HTTPS") and request.headers.get("X-Forwarded-Proto", "http") == "http":
            return redirect(request.url.replace("http://", "https://", 1), code=301)

    @app.after_request
    def set_security_headers(response):
        response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault("Permissions-Policy", "geolocation=(), camera=(), microphone=()")
        response.headers.setdefault("X-XSS-Protection", "0")
        response.headers.pop("Server", None)
        response.headers.setdefault("Cross-Origin-Opener-Policy", "same-origin")
        response.headers.setdefault("Cross-Origin-Resource-Policy", "same-origin")
        response.headers.setdefault("Strict-Transport-Security", "max-age=31536000; includeSubDomains" if app.config.get("FORCE_HTTPS") else "max-age=0")
        response.headers.setdefault("Content-Security-Policy", (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
            "font-src 'self' data: https://fonts.gstatic.com https://cdnjs.cloudflare.com https://cdn.jsdelivr.net; "
            "img-src 'self' data: blob: https:; "
            "connect-src 'self'; "
            "frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "form-action 'self'; "
            "frame-ancestors 'self';"
        ))
        return response

    @app.errorhandler(404)
    def not_found(error):
        return app.jinja_env.get_or_select_template("errors/404.html").render(), 404

    @app.errorhandler(500)
    def server_error(error):
        return app.jinja_env.get_or_select_template("errors/500.html").render(), 500

    with app.app_context():
        db.create_all()
        seed_database(app)

    return app


def seed_database(app):
    from werkzeug.security import generate_password_hash

    if not User.query.first():
        user = User(
            name="Administrator DLH",
            username=app.config["ADMIN_USERNAME"],
            email=app.config["ADMIN_EMAIL"],
            role="superadmin",
        )
        user.set_password(app.config["ADMIN_PASSWORD"])
        db.session.add(user)

    if not NewsCategory.query.first():
        categories = [
            NewsCategory(name="Berita", slug="berita"),
            NewsCategory(name="Artikel", slug="artikel"),
            NewsCategory(name="Kegiatan", slug="kegiatan"),
        ]
        db.session.add_all(categories)
        db.session.flush()

    if not Service.query.first():
        services = [
            Service(title="Perizinan AMDAL", slug="amdal", icon="📑", summary="Analisis dampak lingkungan untuk kegiatan berdampak penting.", content="AMDAL merupakan kajian dampak penting suatu usaha atau kegiatan terhadap lingkungan hidup. Layanan ini membantu pemohon memahami alur, persyaratan, dan tahapan persetujuan lingkungan."),
            Service(title="Perizinan IPLC", slug="iplc", icon="💧", summary="Pengendalian pembuangan air limbah cair.", content="IPLC berfokus pada pengendalian pembuangan air limbah cair agar memenuhi ketentuan teknis dan baku mutu lingkungan."),
            Service(title="Perizinan SPPL", slug="sppl", icon="✅", summary="Surat pernyataan kesanggupan pengelolaan lingkungan.", content="SPPL digunakan untuk usaha atau kegiatan yang tidak wajib AMDAL atau UKL-UPL, tetapi tetap memerlukan komitmen pengelolaan lingkungan."),
            Service(title="Perizinan UKL-UPL", slug="ukl-upl", icon="🌱", summary="Dokumen pengelolaan dan pemantauan lingkungan.", content="UKL-UPL berisi rencana pengelolaan dan pemantauan lingkungan untuk kegiatan yang tidak wajib AMDAL, tetapi tetap memiliki dampak lingkungan."),
        ]
        db.session.add_all(services)

    if not News.query.first():
        cat_berita = NewsCategory.query.filter_by(slug="berita").first()
        cat_artikel = NewsCategory.query.filter_by(slug="artikel").first()
        cat_kegiatan = NewsCategory.query.filter_by(slug="kegiatan").first()
        db.session.add_all([
            News(title="DLH Kota Tasikmalaya Gelar Aksi Bersih Sungai", slug="aksi-bersih-sungai", excerpt="Kolaborasi DLH dan masyarakat dalam menjaga kebersihan sungai.", content="Kegiatan bersih sungai dilakukan untuk meningkatkan kepedulian warga terhadap kebersihan aliran sungai dan pencegahan pencemaran.", image="news-1.svg", category=cat_berita),
            News(title="Sosialisasi Pengelolaan Sampah Rumah Tangga", slug="sosialisasi-sampah-rumah-tangga", excerpt="Edukasi pemilahan sampah dari sumber.", content="DLH mendorong pemilahan sampah dari rumah sebagai dasar pengelolaan sampah yang lebih efektif dan berkelanjutan.", image="news-2.svg", category=cat_artikel),
            News(title="Penanaman Pohon Kawasan Perkotaan", slug="penanaman-pohon-perkotaan", excerpt="Gerakan penghijauan untuk kualitas udara.", content="Program penanaman pohon dilakukan untuk mendukung kualitas udara, ruang hijau, dan kenyamanan kawasan perkotaan.", image="news-3.svg", category=cat_kegiatan),
        ])

    if not Agenda.query.first():
        db.session.add_all([
            Agenda(title="Sosialisasi Pengelolaan Sampah Rumah Tangga", date="2026-06-10", location="Aula DLH Kota Tasikmalaya", description="Edukasi pemilahan dan pengurangan sampah dari rumah."),
            Agenda(title="Aksi Bersih Sungai", date="2026-06-18", location="Kawasan Sungai Ciloseh", description="Kolaborasi warga dan komunitas lingkungan."),
            Agenda(title="Penanaman Pohon Kawasan Perkotaan", date="2026-07-05", location="Taman Kota Tasikmalaya", description="Kegiatan penghijauan untuk kualitas udara."),
        ])

    if not Document.query.first():
        db.session.add_all([
            Document(title="Peraturan Walikota tentang Pengelolaan Lingkungan", category="Peraturan", filename="peraturan_walikota.txt", year=2026, description="Contoh dokumen regulasi lingkungan hidup."),
            Document(title="SOP Instalasi Pengelolaan Air Limbah", category="SOP", filename="sop_air_limbah.txt", year=2026, description="Panduan teknis pengelolaan air limbah."),
            Document(title="SOP Instalasi Pengendali Emisi", category="SOP", filename="sop_pengendali_emisi.txt", year=2026, description="Panduan teknis pengendalian emisi."),
        ])

    if not Gallery.query.first():
        db.session.add_all([
            Gallery(title="Penghijauan Kota", image="gallery-1.svg", type="foto", album="Lingkungan", description="Kegiatan penghijauan dan penataan lingkungan."),
            Gallery(title="Bank Sampah", image="gallery-2.svg", type="foto", album="Sampah", description="Edukasi ekonomi sirkular melalui bank sampah."),
            Gallery(title="Edukasi Lingkungan", image="gallery-3.svg", type="foto", album="Edukasi", description="Kegiatan edukasi bersama masyarakat dan sekolah."),
            Gallery(title="Video Edukasi Lingkungan", image="video-thumb.svg", type="video", video_url="https://www.youtube.com/embed/PrV5ERPC9v0", album="Video", description="Video edukasi pengelolaan lingkungan."),
        ])

    if not LinkItem.query.first():
        db.session.add_all([
            LinkItem(name="Pemerintah Kota Tasikmalaya", url="https://tasikmalayakota.go.id", description="Portal resmi Pemerintah Kota Tasikmalaya.", icon="🏛"),
            LinkItem(name="Dinas Binamarga Kota Tasikmalaya", url="#", description="Tautan instansi terkait infrastruktur jalan.", icon="🛣"),
            LinkItem(name="Dinas Lingkungan Hidup Jawa Barat", url="https://dlh.jabarprov.go.id", description="Portal DLH Provinsi Jawa Barat.", icon="🌿"),
            LinkItem(name="Kementerian Lingkungan Hidup", url="https://www.menlhk.go.id", description="Portal kementerian terkait lingkungan hidup.", icon="🇮🇩"),
            LinkItem(name="Pusat Pengendalian Pembangunan Ekoregion Jawa", url="#", description="Tautan pusat pengendalian ekoregion Jawa.", icon="🗺"),
        ])

    db.session.commit()
