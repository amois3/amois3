"""Handlers package."""
from .start import router as start_router
from .profile import router as profile_router
from .meal import router as meal_router
from .voice import router as voice_router
from .chat import router as chat_router
from .reports import router as reports_router
from .history import router as history_router

# List of all routers
routers = [
    start_router,
    profile_router,
    meal_router,
    voice_router,
    chat_router,
    reports_router,
    history_router,
]

__all__ = ["routers"]
