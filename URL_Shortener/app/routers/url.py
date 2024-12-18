from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.dependencies.db import get_db
from app.schemas.url import URLCreate, URLResponse
from app.crud.url import add_url, delete_url, get_url_by_key
from app.utils.error_handler import ErrorHandler

router = APIRouter()


@router.post("/", response_model=URLResponse)
def create_short_url(url_request: URLCreate, db: Session = Depends(get_db)):
    """
    Endpoint to add a new URL and return its short version.
    """
    result = add_url(db, url_request.url)
    if not result:
        raise HTTPException(status_code=500, detail="Failed to add URL")
    return result


@router.get("/{key}", status_code=302)
def redirect_url(key: str, db: Session = Depends(get_db)):
    """
    Redirects a short URL key to the corresponding long URL.
    """
    
    url_entry = get_url_by_key(db, key)
    
    if not url_entry:
        ErrorHandler.raise_exception(
            "This short URL does not exist", status_code=404)
    return RedirectResponse(url=url_entry.long_url, status_code=302)


@router.delete("/{key_or_url}", status_code=202)
def delete_short_url(key_or_url: str, db: Session = Depends(get_db)):
    """
    Deletes a short URL based on its key or long URL.
    """

    result = delete_url(db, key_or_url)
    return JSONResponse(content=result, status_code=202)
