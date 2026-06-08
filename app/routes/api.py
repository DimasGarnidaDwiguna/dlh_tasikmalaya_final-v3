from flask import Blueprint, request, jsonify
from app.services.search_service import search_all

api_bp = Blueprint("api", __name__)


@api_bp.route("/search")
def search_api():
    keyword = request.args.get("q", "").strip()
    data = search_all(keyword) if keyword else {"news": [], "documents": [], "services": [], "gallery": []}
    return jsonify({
        "news": [{"title": i.title, "url": f"/berita/{i.slug}"} for i in data["news"]],
        "documents": [{"title": i.title, "url": f"/download/{i.filename}"} for i in data["documents"]],
        "services": [{"title": i.title, "url": f"/pelayanan/{i.slug}"} for i in data["services"]],
        "gallery": [{"title": i.title, "url": f"/galeri/{i.type}"} for i in data["gallery"]],
    })
