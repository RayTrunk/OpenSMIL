from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime
from enum import Enum

class MediaType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    OTHER = "other"

class MediaBase(SQLModel):
    name: str
    original_filename: str
    content_type: Optional[str] = None
    size: int
    media_type: MediaType = MediaType.OTHER
    path: str  # Local path or S3 key
    url: Optional[str] = None
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Media(MediaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class MediaCreate(MediaBase):
    pass

class MediaRead(MediaBase):
    id: int
