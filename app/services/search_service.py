from app.models.content import News, Document, Service, Gallery


def search_all(keyword: str) -> dict:
    q = f"%{keyword}%"
    return {
        "news": News.query.filter(News.title.ilike(q)).limit(10).all(),
        "documents": Document.query.filter(Document.title.ilike(q)).limit(10).all(),
        "services": Service.query.filter(Service.title.ilike(q)).limit(10).all(),
        "gallery": Gallery.query.filter(Gallery.title.ilike(q)).limit(10).all(),
    }
