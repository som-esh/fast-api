from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URI = "postgresql://api_db_n7hc_user:nfCmFcmTNNBX4Ryr2qllRychVlwTLRHA@dpg-cfurmohmbjsj9amd0hp0-a.oregon-postgres.render.com/api_db_n7hc"
# "postgresql://postgres:toor@localhost:5432/postgres"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URI
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()