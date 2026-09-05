import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL_FROM_LOCAL = "postgresql+psycopg://user:pw@localhost:5432/pdb"

DATABASE_URL = os.getenv("DATABASE_URL") or DATABASE_URL_FROM_LOCAL

engine = create_engine(url=DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)
