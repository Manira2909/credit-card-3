from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

# .env la irunthu edukkurom - hardcode panna koodathu
DB_USER = os.getenv("DB_USER", "root")
DB_PASS_RAW = os.getenv("DB_PASS", "Manira2909*")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "credit_card_db")

# Special character * irukku, athanala encode pannanum
DB_PASS = quote_plus(DB_PASS_RAW)

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine
engine = create_engine(
    DATABASE_URL, 
    pool_pre_ping=True,  # MySQL disconnect aana auto reconnect
    pool_recycle=3600,
    echo=False  # True na SQL query ellam terminal la varum - debug ku
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()