from pathlib import Path
from uuid import uuid4
from werkzeug.utils import secure_filename

DANGEROUS_EXTENSIONS = {
    "php", "phtml", "phar", "exe", "bat", "cmd", "sh", "js", "html", "htm",
    "svg", "zip", "rar", "7z", "msi", "jar", "py", "rb", "pl", "cgi"
}

IMAGE_MIME_PREFIX = "image/"
DOCUMENT_MIME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "text/plain",
}


def _parts(filename: str) -> list[str]:
    return [part.lower() for part in filename.split(".") if part]


def allowed_file(filename: str, allowed: set[str]) -> bool:
    if not filename or "." not in filename:
        return False

    clean = secure_filename(filename)
    parts = _parts(clean)
    if not parts:
        return False

    ext = parts[-1]
    if ext not in allowed:
        return False

    # Reject files like shell.php.jpg or payload.js.txt.
    if any(part in DANGEROUS_EXTENSIONS for part in parts[:-1]):
        return False

    return True


def _valid_mimetype(file, ext: str) -> bool:
    mimetype = (getattr(file, "mimetype", "") or "").lower()
    if ext in {"jpg", "jpeg", "png", "webp"}:
        return mimetype.startswith(IMAGE_MIME_PREFIX)
    if ext in {"pdf", "docx", "xlsx", "txt"}:
        return mimetype in DOCUMENT_MIME_TYPES or mimetype == "application/octet-stream"
    return False


def save_upload(file, target_dir: Path, allowed: set[str]) -> str | None:
    if not file or not file.filename:
        return None

    if not allowed_file(file.filename, allowed):
        raise ValueError("Format file tidak diizinkan atau nama file mengandung ekstensi berbahaya.")

    target_dir.mkdir(parents=True, exist_ok=True)

    original = secure_filename(file.filename)
    ext = original.rsplit(".", 1)[1].lower()

    if not _valid_mimetype(file, ext):
        raise ValueError("Tipe file tidak sesuai dengan ekstensi yang diupload.")

    stem = original.rsplit(".", 1)[0][:40] or "file"
    filename = f"{stem}-{uuid4().hex[:12]}.{ext}"
    file.save(target_dir / filename)
    return filename
