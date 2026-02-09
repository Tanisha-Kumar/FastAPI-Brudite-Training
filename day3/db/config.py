from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from models.base import Base

DATABASE_URL = "sqlite:///./user.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

sessionLocal = sessionmaker(bind = engine)

Base.metadata.create_all(bind = engine)