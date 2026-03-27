from fastapi import APIRouter
from app.api.v1.endpoints import players, auth, users, media, playlists, smil

api_router = APIRouter()
api_router.include_router(auth.router, tags=["Auth"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(media.router, prefix="/media", tags=["Media"])
api_router.include_router(playlists.router, prefix="/playlists", tags=["Playlists"])
api_router.include_router(players.router, prefix="/players", tags=["Players"])
api_router.include_router(smil.router, prefix="/smil", tags=["SMIL"])
