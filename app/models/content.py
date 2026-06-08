from datetime import datetime
from app.extensions import db


class BaseTimeMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Service(db.Model, BaseTimeMixin):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    slug = db.Column(db.String(160), unique=True, nullable=False, index=True)
    icon = db.Column(db.String(30), default="🌿")
    summary = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, default=True)


class NewsCategory(db.Model, BaseTimeMixin):
    __tablename__ = "news_categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)


class News(db.Model, BaseTimeMixin):
    __tablename__ = "news"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(220), nullable=False)
    slug = db.Column(db.String(180), unique=True, nullable=False, index=True)
    excerpt = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), default="news-1.svg")
    category_id = db.Column(db.Integer, db.ForeignKey("news_categories.id"))
    category = db.relationship("NewsCategory")
    author = db.Column(db.String(120), default="Admin DLH")
    views = db.Column(db.Integer, default=0)
    is_published = db.Column(db.Boolean, default=True)


class Agenda(db.Model, BaseTimeMixin):
    __tablename__ = "agenda"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(220), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(220), nullable=False)
    description = db.Column(db.Text)


class Document(db.Model, BaseTimeMixin):
    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(220), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255))
    downloads = db.Column(db.Integer, default=0)


class Gallery(db.Model, BaseTimeMixin):
    __tablename__ = "gallery"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(20), default="foto")
    video_url = db.Column(db.String(255))
    album = db.Column(db.String(120), default="Umum")
    description = db.Column(db.String(255))


class LinkItem(db.Model, BaseTimeMixin):
    __tablename__ = "links"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(180), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    icon = db.Column(db.String(30), default="🔗")


class ContactMessage(db.Model, BaseTimeMixin):
    __tablename__ = "contacts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False)
    email = db.Column(db.String(160), nullable=False)
    subject = db.Column(db.String(180), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(40), default="Baru")


class Complaint(db.Model, BaseTimeMixin):
    __tablename__ = "complaints"

    id = db.Column(db.Integer, primary_key=True)
    ticket_number = db.Column(db.String(40), unique=True, index=True)
    name = db.Column(db.String(140), nullable=False)
    email = db.Column(db.String(160), nullable=False)
    phone = db.Column(db.String(40))
    category = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(220), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(40), default="Masuk")
    admin_response = db.Column(db.Text)


class VisitorLog(db.Model):
    __tablename__ = "visitor_logs"

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(255))
    ip_address = db.Column(db.String(80))
    user_agent = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
