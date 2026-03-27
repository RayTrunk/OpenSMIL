from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime

class PlayerBase(SQLModel):
    name: str
    mac_address: str = Field(index=True, unique=True)
    description: Optional[str] = None
    last_seen: Optional[datetime] = None
    is_active: bool = True
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    playlist_id: Optional[int] = Field(default=None, foreign_key="playlist.id")

class Player(PlayerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class PlayerCreate(PlayerBase):
    pass

class PlayerRead(PlayerBase):
    id: int
