# init_db.py

from database.db_init import engine
from database.models import Base

# Create all tables
Base.metadata.create_all(bind=engine)
print(" Database initialized with tables.")

