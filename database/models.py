from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class SyntheticImage(Base):
    __tablename__ = "synthetic_images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    generator_type = Column(String)
    resolution = Column(String)
    notes = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)