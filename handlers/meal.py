"""Meal scanning handlers."""
import random
from aiogram import Router, F
from aiogram.types import Message
from database.mongodb import db
from database.models import Meal
from services import GeminiService, ImageOptimizer, CostTracker
from utils import format_meal, MEAL_REACTIONS

router = Router()
gemini = GeminiService()
optimizer = ImageOptimizer()
tracker = CostTracker()

@router.message(F.photo)
async def photo_handler(msg: Message):
    user = await db.get_or_create_user(msg.from_user.id)
    st = await msg.answer("⏳ Анализирую...")
    try:
        photo = msg.photo[-1]
        file = await msg.bot.get_file(photo.file_id)
        data = await msg.bot.download_file(file.file_path)
        b64 = optimizer.optimize_and_encode(data.read())
        foods, nutr, anl, score, typ = await gemini.analyze_meal_from_photo(b64, msg.caption, user)
        meal = Meal(user_id=user.id, telegram_id=msg.from_user.id, meal_type=typ, foods=foods, total_nutrition=nutr, photo_file_id=photo.file_id, description=msg.caption, ai_analysis=anl, health_score=score)
        await db.create_meal(meal)
        await st.delete()
        await msg.answer(format_meal(meal, user), parse_mode="Markdown")
    except Exception as e:
        await st.edit_text(f"❌ {e}")

@router.message(F.text & ~F.command)
async def text_handler(msg: Message):
    user = await db.get_or_create_user(msg.from_user.id)
    if user.in_chat_mode:
        return
    st = await msg.answer("⏳ Анализирую...")
    try:
        foods, nutr, anl, score, typ = await gemini.analyze_meal_from_text(msg.text, user)
        meal = Meal(user_id=user.id, telegram_id=msg.from_user.id, meal_type=typ, foods=foods, total_nutrition=nutr, description=msg.text, ai_analysis=anl, health_score=score)
        await db.create_meal(meal)
        await st.delete()
        await msg.answer(format_meal(meal, user), parse_mode="Markdown")
    except Exception as e:
        await st.edit_text(f"❌ {e}")
