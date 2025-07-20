import sys
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base, SyntheticImage

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Ensure DB directory exists
os.makedirs("data/synthetic", exist_ok=True)

# Database connection
DATABASE_URL = "sqlite:///data/synthetic/synthetic_images.db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

# Initialize the DB (create tables if not exists)
def init_db():
    Base.metadata.create_all(bind=engine)

# Save metadata to the database
def save_to_database(filename, generator_type, resolution, notes=""):
    session = SessionLocal()
    try:
        image = SyntheticImage(
            filename=filename,
            generator_type=generator_type,
            resolution=resolution,
            notes=notes,
            created_at=datetime.utcnow()
        )
        session.add(image)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"[DB ERROR] {e}")
    finally:
        session.close()

