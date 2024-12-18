from sqlalchemy.orm import Session
from app.models.url import URL
from app.utils.url_shortener import generate_short_url_key
from app.schemas.url import URLResponse

def add_url(db: Session, long_url: str) -> URLResponse:
    """
    Adds a new long URL to the database and generates a short URL with collision detection.
    """

    url_db = db.query(URL).filter(URL.long_url == long_url).first()
    if url_db:
        return URLResponse(
            msg="URL already exists",
            key=url_db.key,
            short_url=url_db.short_url,
            long_url=url_db.long_url
        )

    while True:
        key = generate_short_url_key(long_url)
        short_url = f"https://localhost:5000/{key}"

        existing_key = db.query(URL).filter(URL.key == key).first()
        if not existing_key: 
            break

    new_url = URL(key=key, short_url=short_url, long_url=long_url)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    return URLResponse(
        msg="Successfully Added to DB",
        key=key,
        short_url=short_url,
        long_url=long_url
    )
