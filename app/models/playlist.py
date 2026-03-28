from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

class PlaylistItemBase(SQLModel):
    media_id: int = Field(foreign_key="media.id")
    playlist_id: Optional[int] = Field(default=None, foreign_key="playlist.id")
    position: int = 0
    duration: int = 10  # seconds

class PlaylistItem(PlaylistItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    playlist: "Playlist" = Relationship(back_populates="items")
    media: "Media" = Relationship()

class PlaylistBase(SQLModel):
    name: str
    description: Optional[str] = None
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")

class Playlist(PlaylistBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    items: List[PlaylistItem] = Relationship(back_populates="playlist")

class PlaylistCreate(PlaylistBase):
    pass

class PlaylistItemCreate(PlaylistItemBase):
    pass

from app.models.media import MediaRead

class PlaylistItemRead(PlaylistItemBase):
    id: int
    media: Optional[MediaRead] = None

class PlaylistRead(PlaylistBase):
    id: int
    items: List[PlaylistItemRead] = []
