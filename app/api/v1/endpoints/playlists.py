from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.db import get_session
from app.models.playlist import (
    Playlist, PlaylistCreate, PlaylistRead,
    PlaylistItem, PlaylistItemCreate, PlaylistItemRead
)
from app.models.user import User, UserRole
from app.api import deps

router = APIRouter()

@router.post("/", response_model=PlaylistRead)
def create_playlist(
    playlist_in: PlaylistCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(deps.get_current_user)
):
    playlist = Playlist.from_orm(playlist_in)
    playlist.owner_id = current_user.id
    session.add(playlist)
    session.commit()
    session.refresh(playlist)
    return playlist

@router.get("/", response_model=List[PlaylistRead])
def read_playlists(
    session: Session = Depends(get_session),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.role == UserRole.ADMIN:
        playlists = session.exec(select(Playlist)).all()
    else:
        playlists = session.exec(select(Playlist).where(Playlist.owner_id == current_user.id)).all()
    return playlists

@router.get("/{playlist_id}", response_model=PlaylistRead)
def read_playlist(
    playlist_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(deps.get_current_user)
):
    playlist = session.get(Playlist, playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    if current_user.role != UserRole.ADMIN and playlist.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return playlist

@router.put("/{playlist_id}", response_model=PlaylistRead)
def update_playlist(
    playlist_id: int,
    playlist_in: PlaylistCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(deps.get_current_user)
):
    playlist = session.get(Playlist, playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    if current_user.role != UserRole.ADMIN and playlist.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough privileges")
    
    playlist_data = playlist_in.dict(exclude_unset=True)
    for key, value in playlist_data.items():
        setattr(playlist, key, value)
    
    session.add(playlist)
    session.commit()
    session.refresh(playlist)
    return playlist

@router.delete("/{playlist_id}")
def delete_playlist(
    playlist_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(deps.get_current_user)
):
    playlist = session.get(Playlist, playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    if current_user.role != UserRole.ADMIN and playlist.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough privileges")
    
    session.delete(playlist)
    session.commit()
    return {"message": "Playlist deleted"}

@router.post("/{playlist_id}/items", response_model=PlaylistItemRead)
def add_playlist_item(
    playlist_id: int,
    item_in: PlaylistItemCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(deps.get_current_user)
):
    playlist = session.get(Playlist, playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    if current_user.role != UserRole.ADMIN and playlist.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough privileges")
    
    item = PlaylistItem.from_orm(item_in)
    item.playlist_id = playlist_id
    session.add(item)
    session.commit()
    session.refresh(item)
    return item
