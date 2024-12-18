from pydantic import BaseModel, HttpUrl

class URLCreate(BaseModel):
    url: HttpUrl

class URLResponse(BaseModel):
    msg: str
    key: str
    short_url: str
    long_url: str

    class Config:
        from_attributes = True
