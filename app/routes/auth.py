from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models.user import User

auth_bp = Blueprint("auth", __name__)

# Simple in-memory login throttle for presentation and local deployment.
# For production multi-worker deployments, use Redis or a WAF rate limiter.
_LOGIN_ATTEMPTS = {}
MAX_LOGIN_ATTEMPTS = 6
LOCKOUT_MINUTES = 10


def _client_key():
    forwarded = request.headers.get("X-Forwarded-For", "")
    ip = forwarded.split(",")[0].strip() if forwarded else request.remote_addr
    return ip or "unknown"


def _is_blocked(key):
    record = _LOGIN_ATTEMPTS.get(key)
    if not record:
        return False
    count, first_attempt = record
    if datetime.utcnow() - first_attempt > timedelta(minutes=LOCKOUT_MINUTES):
        _LOGIN_ATTEMPTS.pop(key, None)
        return False
    return count >= MAX_LOGIN_ATTEMPTS


def _record_failed_login(key):
    count, first_attempt = _LOGIN_ATTEMPTS.get(key, (0, datetime.utcnow()))
    if datetime.utcnow() - first_attempt > timedelta(minutes=LOCKOUT_MINUTES):
        count, first_attempt = 0, datetime.utcnow()
    _LOGIN_ATTEMPTS[key] = (count + 1, first_attempt)


@auth_bp.route("/admin/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))

    key = _client_key()
    if _is_blocked(key):
        flash("Terlalu banyak percobaan login. Coba lagi beberapa menit lagi.", "danger")
        return render_template("admin/login.html"), 429

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()

        if user and user.is_active and user.check_password(password):
            _LOGIN_ATTEMPTS.pop(key, None)
            user.last_login = datetime.utcnow()
            db.session.commit()
            login_user(user)
            return redirect(url_for("admin.dashboard"))

        _record_failed_login(key)
        flash("Username atau password salah.", "danger")

    return render_template("admin/login.html")


@auth_bp.route("/admin/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
