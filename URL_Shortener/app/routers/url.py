from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.db import get_db
from app.schemas.url import URLCreate, URLResponse
from app.crud.url import add_url

router = APIRouter()

@router.post("/urls/", response_model=URLResponse)
def create_short_url(url_request: URLCreate, db: Session = Depends(get_db)):
    """
    Endpoint to add a new URL and return its short version.
    """
    result = add_url(db, url_request.url)
    if not result:
        raise HTTPException(status_code=500, detail="Failed to add URL")
    return result
