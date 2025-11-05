"""Profile management."""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from database.mongodb import db
from utils import format_user_profile, calculate_bmr, calculate_tdee, calculate_target_calories, calculate_macros

router = Router()

@router.message(Command("profile"))
async def prof(msg: Message):
    user = await db.get_or_create_user(msg.from_user.id)
    await msg.answer(format_user_profile(user), parse_mode="Markdown")

@router.message(Command("setage"))
async def age(msg: Message):
    user = await db.get_or_create_user(msg.from_user.id)
    try:
        user.age = int(msg.text.split()[1])
        await _recalc(user)
        await db.update_user(user)
        await msg.answer("✅ Возраст обновлен")
    except:
        await msg.answer("Использование: /setage 25")

@router.message(Command("setheight"))
async def height(msg: Message):
    user = await db.get_or_create_user(msg.from_user.id)
    try:
        user.height = float(msg.text.split()[1])
        await _recalc(user)
        await db.update_user(user)
        await msg.answer("✅ Рост обновлен")
    except:
        await msg.answer("Использование: /setheight 175")

@router.message(Command("setweight"))
async def weight(msg: Message):
    user = await db.get_or_create_user(msg.from_user.id)
    try:
        user.weight = float(msg.text.split()[1])
        await _recalc(user)
        await db.update_user(user)
        await msg.answer("✅ Вес обновлен")
    except:
        await msg.answer("Использование: /setweight 70")

async def _recalc(user):
    if all([user.gender, user.age, user.height, user.weight]):
        user.bmr = calculate_bmr(user.gender, user.age, user.height, user.weight)
        if user.activity_level:
            user.tdee = calculate_tdee(user.bmr, user.activity_level)
            if user.goal:
                user.target_calories = calculate_target_calories(user.tdee, user.goal)
                p, c, f = calculate_macros(user.target_calories, user.goal)
                user.target_protein, user.target_carbs, user.target_fats = p, c, f
