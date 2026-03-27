from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.db import get_session
from app.models.player import Player, PlayerRead, PlayerCreate
from app.models.user import User, UserRole
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[PlayerRead])
def read_players(
    session: Session = Depends(get_session),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.role == UserRole.ADMIN:
        players = session.exec(select(Player)).all()
    else:
        players = session.exec(select(Player).where(Player.owner_id == current_user.id)).all()
    return players

@router.post("/", response_model=PlayerRead)
def create_player(
    player: PlayerCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(deps.get_current_user)
):
    db_player = Player.from_orm(player)
    db_player.owner_id = current_user.id
    session.add(db_player)
    session.commit()
    session.refresh(db_player)
    return db_player

@router.put("/{player_id}", response_model=PlayerRead)
def update_player(
    player_id: int,
    player_in: PlayerCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(deps.get_current_user)
):
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    if current_user.role != UserRole.ADMIN and player.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough privileges")
    
    player_data = player_in.dict(exclude_unset=True)
    for key, value in player_data.items():
        setattr(player, key, value)
    
    session.add(player)
    session.commit()
    session.refresh(player)
    return player

@router.get("/{player_id}", response_model=PlayerRead)
def read_player(
    player_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(deps.get_current_user)
):
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    if current_user.role != UserRole.ADMIN and player.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return player

@router.delete("/{player_id}")
def delete_player(
    player_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(deps.get_current_user)
):
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    if current_user.role != UserRole.ADMIN and player.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough privileges")
    
    session.delete(player)
    session.commit()
    return {"message": "Player deleted"}
