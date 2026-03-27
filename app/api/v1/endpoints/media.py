import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlmodel import Session, select
from app.core.db import get_session
from app.models.media import Media, MediaRead, MediaType
from app.models.user import User, UserRole
from app.api import deps
from app.services.storage import get_storage_service, StorageService

router = APIRouter()

def get_media_type(content_type: Optional[str]) -> MediaType:
    if not content_type:
        return MediaType.OTHER
    if content_type.startswith("image/"):
        return MediaType.IMAGE
    if content_type.startswith("video/"):
        return MediaType.VIDEO
    if content_type.startswith("audio/"):
        return MediaType.AUDIO
    return MediaType.OTHER

@router.post("/", response_model=MediaRead)
async def upload_media(
    name: str = Form(...),
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    current_user: User = Depends(deps.get_current_user),
    storage: StorageService = Depends(get_storage_service)
):
    # Generate unique filename
    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    
    # Save file
    path = await storage.upload(file, filename)
    url = storage.get_url(path)
    
    # Get file size (from UploadFile)
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)
    
    # Save metadata
    db_media = Media(
        name=name,
        original_filename=file.filename,
        content_type=file.content_type,
        size=size,
        media_type=get_media_type(file.content_type),
        path=path,
        url=url,
        owner_id=current_user.id
    )
    session.add(db_media)
    session.commit()
    session.refresh(db_media)
    return db_media

@router.get("/", response_model=List[MediaRead])
def read_media(
    session: Session = Depends(get_session),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.role == UserRole.ADMIN:
        media = session.exec(select(Media)).all()
    else:
        media = session.exec(select(Media).where(Media.owner_id == current_user.id)).all()
    return media

@router.delete("/{media_id}")
def delete_media(
    media_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(deps.get_current_user),
    storage: StorageService = Depends(get_storage_service)
):
    media = session.get(Media, media_id)
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    if current_user.role != UserRole.ADMIN and media.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough privileges")
    
    # Delete file
    storage.delete(media.path)
    
    # Delete metadata
    session.delete(media)
    session.commit()
    return {"message": "Media deleted successfully"}
