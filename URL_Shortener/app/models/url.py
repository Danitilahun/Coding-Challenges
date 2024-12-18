from sqlalchemy import Column, Integer, String
from app.db import Base


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    short_url = Column(String, unique=True, index=True)
    long_url = Column(String, nullable=False)
