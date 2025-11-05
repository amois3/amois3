"""Voice messages - Whisper API."""
from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.voice)
async def voice_msg(msg: Message):
    """Handle voice messages."""
    await msg.answer("🎙️ Голосовые сообщения скоро будут доступны!")
