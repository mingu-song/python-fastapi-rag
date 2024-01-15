from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import text
from sqlalchemy_utils import database_exists, create_database
from pgvector.sqlalchemy import Vector
from dotenv import load_dotenv
import os
import urllib.parse

load_dotenv()

POSTGRES_USERNAME = os.getenv('POSTGRES_USERNAME')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '6432')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'postgres')
encoded_password = urllib.parse.quote_plus(POSTGRES_PASSWORD)

database_url = f"postgresql://{POSTGRES_USERNAME}:{encoded_password}@{POSTGRES_HOST}:{POSTGRES_PORT}/{DATABASE_NAME}"
engine = create_engine(database_url)

if not database_exists(engine.url):
    create_database(engine.url)


SessionLocal = sessionmaker(autoflush=False, bind=engine, autocommit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base()


class Files(Base):
    __tablename__ = 'files'
    file_id = Column(Integer, primary_key=True)
    file_name = Column(String(255))
    file_content = Column(Text)


class FileChunk(Base):
    __tablename__ = 'file_chunks'
    chunk_id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey('files.file_id'))
    chunk_text = Column(Text)
    embedding_vector = Column(Vector(1536))


with sessionmaker(bind=engine)() as session:
    session.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))
    session.commit()


try:
    Base.metadata.create_all(engine)
except Exception as e:
    print(e)
