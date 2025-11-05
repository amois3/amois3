"""AI chat mode."""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from database.mongodb import db
from database.models import ChatMessage
from services import GeminiService

router = Router()
gemini = GeminiService()

@router.message(Command("chat"))
async def chat_on(msg: Message):
    user = await db.get_or_create_user(msg.from_user.id)
    user.in_chat_mode = True
    await db.update_user(user)
    await msg.answer("💬 AI-чат активирован. /stopchat для выхода", parse_mode="Markdown")

@router.message(Command("stopchat"))
async def chat_off(msg: Message):
    user = await db.get_or_create_user(msg.from_user.id)
    user.in_chat_mode = False
    await db.update_user(user)
    await msg.answer("✅ Чат деактивирован")
