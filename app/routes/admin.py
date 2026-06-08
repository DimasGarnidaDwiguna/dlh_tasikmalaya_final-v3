from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app.extensions import db
from app.models.user import User
from app.models.content import (
    Service, NewsCategory, News, Agenda, Document, Gallery, LinkItem,
    ContactMessage, Complaint, VisitorLog
)
from app.services.upload_service import save_upload
from app.utils.helpers import valid_year

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/")
@login_required
def dashboard():
    stats = {
        "news": News.query.count(),
        "documents": Document.query.count(),
        "contacts": ContactMessage.query.count(),
        "complaints": Complaint.query.count(),
        "visitors": VisitorLog.query.count(),
    }
    latest_contacts = ContactMessage.query.order_by(ContactMessage.id.desc()).limit(5).all()
    latest_complaints = Complaint.query.order_by(Complaint.id.desc()).limit(5).all()
    return render_template("admin/dashboard.html", stats=stats, latest_contacts=latest_contacts, latest_complaints=latest_complaints)


@admin_bp.route("/contacts")
@login_required
def contacts():
    page = request.args.get("page", 1, type=int)
    items = ContactMessage.query.order_by(ContactMessage.id.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template("admin/contacts.html", items=items)


@admin_bp.route("/complaints")
@login_required
def complaints():
    page = request.args.get("page", 1, type=int)
    items = Complaint.query.order_by(Complaint.id.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template("admin/complaints.html", items=items)


@admin_bp.route("/complaints/<int:item_id>/status", methods=["POST"])
@login_required
def complaint_status(item_id):
    allowed_status = {"Masuk", "Diproses", "Selesai", "Ditolak"}
    item = Complaint.query.get_or_404(item_id)
    status = request.form.get("status", item.status)
    if status not in allowed_status:
        flash("Status pengaduan tidak valid.", "danger")
        return redirect(url_for("admin.complaints"))
    item.status = status
    item.admin_response = request.form.get("admin_response", item.admin_response)
    db.session.commit()
    flash("Status pengaduan diperbarui.", "success")
    return redirect(url_for("admin.complaints"))


@admin_bp.route("/services", methods=["GET", "POST"])
@login_required
def services():
    if request.method == "POST":
        item = Service(
            title=request.form["title"],
            slug=request.form["slug"],
            icon=request.form.get("icon", "🌿"),
            summary=request.form["summary"],
            content=request.form["content"],
            is_active=bool(request.form.get("is_active", True)),
        )
        db.session.add(item)
        db.session.commit()
        flash("Layanan berhasil ditambahkan.", "success")
        return redirect(url_for("admin.services"))

    items = Service.query.order_by(Service.id.desc()).all()
    return render_template("admin/services.html", items=items)


@admin_bp.route("/services/<int:item_id>/delete", methods=["POST"])
@login_required
def service_delete(item_id):
    item = Service.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash("Layanan berhasil dihapus.", "success")
    return redirect(url_for("admin.services"))


@admin_bp.route("/news", methods=["GET", "POST"])
@login_required
def news():
    if request.method == "POST":
        image = "news-1.svg"
        file = request.files.get("image")
        if file and file.filename:
            try:
                image = save_upload(file, current_app.config["UPLOAD_ROOT"] / "news", current_app.config["ALLOWED_IMAGE_EXTENSIONS"])
            except ValueError as exc:
                flash(str(exc), "danger")
                return redirect(url_for("admin.news"))
        category = NewsCategory.query.get(request.form.get("category_id", type=int))
        item = News(
            title=request.form["title"],
            slug=request.form["slug"],
            excerpt=request.form["excerpt"],
            content=request.form["content"],
            image=image,
            category=category,
            author=current_user.name,
            is_published=bool(request.form.get("is_published", True)),
        )
        db.session.add(item)
        db.session.commit()
        flash("Berita berhasil ditambahkan.", "success")
        return redirect(url_for("admin.news"))

    page = request.args.get("page", 1, type=int)
    items = News.query.order_by(News.id.desc()).paginate(page=page, per_page=10, error_out=False)
    categories = NewsCategory.query.all()
    return render_template("admin/news.html", items=items, categories=categories)


@admin_bp.route("/news/<int:item_id>/delete", methods=["POST"])
@login_required
def news_delete(item_id):
    item = News.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash("Berita berhasil dihapus.", "success")
    return redirect(url_for("admin.news"))


@admin_bp.route("/documents", methods=["GET", "POST"])
@login_required
def documents():
    if request.method == "POST":
        year = request.form.get("year", "").strip()
        if not valid_year(year):
            flash("Tahun dokumen harus 4 digit angka, contoh 2026.", "danger")
            return redirect(url_for("admin.documents"))

        filename = request.form.get("filename", "").strip()
        file = request.files.get("file")
        if file and file.filename:
            try:
                filename = save_upload(file, current_app.config["UPLOAD_ROOT"] / "documents", current_app.config["ALLOWED_DOCUMENT_EXTENSIONS"])
            except ValueError as exc:
                flash(str(exc), "danger")
                return redirect(url_for("admin.documents"))

        if not filename:
            flash("File dokumen wajib diupload atau nama file manual wajib diisi.", "danger")
            return redirect(url_for("admin.documents"))

        item = Document(
            title=request.form["title"],
            category=request.form["category"],
            filename=filename,
            year=int(year),
            description=request.form.get("description", ""),
        )
        db.session.add(item)
        db.session.commit()
        flash("Dokumen berhasil ditambahkan.", "success")
        return redirect(url_for("admin.documents"))

    items = Document.query.order_by(Document.id.desc()).all()
    return render_template("admin/documents.html", items=items)


@admin_bp.route("/gallery", methods=["GET", "POST"])
@login_required
def gallery():
    if request.method == "POST":
        image = "gallery-1.svg"
        file = request.files.get("image")
        if file and file.filename:
            try:
                image = save_upload(file, current_app.config["UPLOAD_ROOT"] / "gallery", current_app.config["ALLOWED_IMAGE_EXTENSIONS"])
            except ValueError as exc:
                flash(str(exc), "danger")
                return redirect(url_for("admin.gallery"))
        item = Gallery(
            title=request.form["title"],
            image=image,
            type=request.form.get("type", "foto"),
            video_url=request.form.get("video_url", ""),
            album=request.form.get("album", "Umum"),
            description=request.form.get("description", ""),
        )
        db.session.add(item)
        db.session.commit()
        flash("Galeri berhasil ditambahkan.", "success")
        return redirect(url_for("admin.gallery"))

    items = Gallery.query.order_by(Gallery.id.desc()).all()
    return render_template("admin/gallery.html", items=items)


@admin_bp.route("/links", methods=["GET", "POST"])
@login_required
def links():
    if request.method == "POST":
        item = LinkItem(
            name=request.form["name"],
            url=request.form["url"],
            icon=request.form.get("icon", "🔗"),
            description=request.form.get("description", ""),
        )
        db.session.add(item)
        db.session.commit()
        flash("Link berhasil ditambahkan.", "success")
        return redirect(url_for("admin.links"))

    items = LinkItem.query.order_by(LinkItem.id.desc()).all()
    return render_template("admin/links.html", items=items)


@admin_bp.route("/settings")
@login_required
def settings():
    users = User.query.order_by(User.id.asc()).all()
    return render_template("admin/settings.html", users=users)
