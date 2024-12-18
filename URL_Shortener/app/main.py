from fastapi import FastAPI
from app.routers import url
from app.db import engine, Base

app = FastAPI(title="URL Shortener API", version="1.0.0")

Base.metadata.create_all(bind=engine)

app.include_router(url.router, prefix="/api", tags=["URL Shortener"])

@app.get("/")
def root():
    return {"message": "Welcome to the URL Shortener API!"}
