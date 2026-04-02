from fastapi import APIRouter
from app.api.v1.endpoints import auth, interaction, chat, tools

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(interaction.router, prefix="/interaction", tags=["interaction"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(tools.router, prefix="/tools", tags=["tools"])


