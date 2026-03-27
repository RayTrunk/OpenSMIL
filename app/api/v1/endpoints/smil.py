from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session, select
from app.core.db import get_session
from app.models.player import Player
from app.models.playlist import Playlist, PlaylistItem
from app.models.media import MediaType
from app.services.smil_builder import SMILBuilder
from datetime import datetime

router = APIRouter()

@router.get("/{mac_address}/smil.xml")
def get_player_smil(
    mac_address: str,
    session: Session = Depends(get_session)
):
    # Find player by MAC
    player = session.exec(select(Player).where(Player.mac_address == mac_address)).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    # Update last seen
    player.last_seen = datetime.utcnow()
    session.add(player)
    session.commit()
    
    if not player.playlist_id:
        # Return empty SMIL or default content
        builder = SMILBuilder()
        builder.add_region("main")
        return Response(content=builder.get_smil_string(), media_type="application/smil+xml")
    
    playlist = session.get(Playlist, player.playlist_id)
    
    # Build SMIL
    builder = SMILBuilder()
    builder.add_region("main")
    
    # Add sequence
    from lxml import etree
    seq = etree.SubElement(builder.body, "seq", repeatCount="indefinite")
    
    # Sort items by position
    items = sorted(playlist.items, key=lambda x: x.position)
    
    for item in items:
        media = item.media
        if media.media_type == MediaType.VIDEO:
            etree.SubElement(seq, "video", src=media.url, region="main", dur=f"{item.duration}s")
        else:
            etree.SubElement(seq, "img", src=media.url, region="main", dur=f"{item.duration}s")
            
    return Response(content=builder.get_smil_string(), media_type="application/smil+xml")
