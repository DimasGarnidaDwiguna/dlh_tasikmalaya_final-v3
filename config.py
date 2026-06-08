import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"

load_dotenv(BASE_DIR / ".env")


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-secret-key-before-deploy")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://root:@localhost:3306/dlh_tasikmalaya?charset=utf8mb4"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
    }

    WTF_CSRF_ENABLED = True
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    UPLOAD_ROOT = BASE_DIR / "app" / "static" / "uploads"

    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@dlh.local")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")

    SITE_NAME = "Dinas Lingkungan Hidup Kota Tasikmalaya"
    SITE_DESCRIPTION = "Portal digital layanan, informasi, dokumen, galeri, dan pengaduan lingkungan hidup Kota Tasikmalaya."

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "False").lower() == "true"
    FORCE_HTTPS = os.environ.get("FORCE_HTTPS", "False").lower() == "true"

    ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
    ALLOWED_DOCUMENT_EXTENSIONS = {"pdf", "docx", "xlsx", "txt"}

    SESSION_COOKIE_NAME = "dlh_session"
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = "Lax"
    REMEMBER_COOKIE_SECURE = SESSION_COOKIE_SECURE
    PERMANENT_SESSION_LIFETIME = 3600
