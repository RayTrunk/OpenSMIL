from sqlmodel import create_engine, SQLModel, Session
from app.core.config import settings

# Import all models here so SQLModel knows about them
from app.models.user import User
from app.models.player import Player
from app.models.media import Media
from app.models.playlist import Playlist, PlaylistItem

# For SQLite, we need to allow multithreading
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
