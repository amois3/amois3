"""History and search."""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from database.mongodb import db

router = Router()

@router.message(Command("history"))
async def hist(msg: Message):
    meals = await db.get_recent_meals(msg.from_user.id, 5)
    if not meals:
        await msg.answer("📝 История пуста")
        return
    text = "📜 *Последние приемы:*\n\n"
    for i, m in enumerate(meals, 1):
        foods = ", ".join([f.name for f in m.foods[:2]])
        text += f"{i}. {m.meal_time.strftime('%d.%m %H:%M')} - {foods} ({m.total_nutrition.calories:.0f} ккал)\n"
    await msg.answer(text, parse_mode="Markdown")

@router.message(Command("search"))
async def search(msg: Message):
    q = msg.text.replace("/search", "").strip()
    if not q:
        await msg.answer("Использование: /search пицца")
        return
    meals = await db.search_meals(msg.from_user.id, q, 5)
    if not meals:
        await msg.answer(f"🔍 Ничего не найдено: {q}")
        return
    text = f"🔍 *Найдено:*\n\n"
    for m in meals:
        text += f"• {m.meal_time.strftime('%d.%m %H:%M')} - {', '.join([f.name for f in m.foods[:2]])}\n"
    await msg.answer(text, parse_mode="Markdown")
