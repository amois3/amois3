"""Reports and graphs."""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile
from datetime import datetime
from database.mongodb import db
from database.models import Nutrition
from services import GraphGenerator

router = Router()
graphs = GraphGenerator()

@router.message(Command("graph"))
async def graph_cmd(msg: Message):
    user = await db.get_or_create_user(msg.from_user.id)
    buf = await graphs.generate_nutrition_graph(msg.from_user.id, 7, user)
    photo = BufferedInputFile(buf.read(), "graph.png")
    await msg.answer_photo(photo, caption="📊 График за неделю")

@router.message(Command("report"))
async def report_cmd(msg: Message):
    today = datetime.utcnow()
    meals = await db.get_meals_for_period(msg.from_user.id, today.replace(hour=0,minute=0), today)
    if not meals:
        await msg.answer("📊 Нет данных за сегодня")
        return
    total = Nutrition()
    for m in meals:
        total.calories += m.total_nutrition.calories
        total.protein += m.total_nutrition.protein
        total.carbs += m.total_nutrition.carbs
        total.fats += m.total_nutrition.fats
    text = f"📊 *Отчет за сегодня*\n\n"
    text += f"Приемов: {len(meals)}\n"
    text += f"🔥 {total.calories:.0f} ккал\n"
    text += f"🥩 {total.protein:.1f}г Б\n"
    text += f"🍞 {total.carbs:.1f}г У\n"
    text += f"🥑 {total.fats:.1f}г Ж"
    await msg.answer(text, parse_mode="Markdown")

@router.message(Command("cost"))
async def cost_cmd(msg: Message):
    daily = await db.get_daily_cost(msg.from_user.id)
    total = await db.get_total_cost(msg.from_user.id)
    text = f"💰 *Расходы OpenAI*\n\nСегодня: ${daily:.4f}\nВсего: ${total:.4f}"
    await msg.answer(text, parse_mode="Markdown")
