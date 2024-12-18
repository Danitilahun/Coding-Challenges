from sqlalchemy.orm import Session
from app.db import SessionLocal

def get_db():
    """
    Dependency for database sessions.
    Opens a session and ensures it is closed after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
