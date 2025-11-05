"""Start and help command handlers."""
from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from database.mongodb import db

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Handle /start command."""
    user = await db.get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    text = f"""Привет, {message.from_user.first_name}! 👋

Я - твой персональный AI-нутрициолог. Помогу отслеживать питание и давать рекомендации.

🔥 *Что я умею:*
• 📸 Анализировать еду по фото (GPT-4o Vision)
• ✏️ Считать КБЖУ из текстового описания
• 🎙️ Понимать голосовые сообщения
• 💬 Отвечать на вопросы в AI-чате
• 📊 Формировать отчеты с графиками
• 📈 Отслеживать прогресс

📸 *Просто отправь фото блюда или опиши текстом!*

Используй /help для подробной информации.
Настрой /profile для точных рекомендаций."""

    await message.answer(text, parse_mode="Markdown")


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Handle /help command."""
    text = """📚 *Справка по командам*

*Основные команды:*
/start - Начать работу
/help - Эта справка
/profile - Настроить профиль
/report - Отчет за сегодня
/week - Отчет за неделю
/graph - График питания
/weight - График веса
/history - История приемов пищи
/search <текст> - Поиск в истории
/chat - AI-чат режим
/stopchat - Выйти из чата
/cost - Статистика расходов

*Как использовать:*

📸 *Фото еды:* Просто отправь фото
🎙️ *Голос:* Запиши голосовое описание
✏️ *Текст:* Опиши что съел

💬 *AI-чат:* /chat для вопросов нутрициологу
📊 *Графики:* /graph и /weight для визуализации

_Автоматические отчеты: ежедневно в 21:00, еженедельно по понедельникам в 9:00_"""

    await message.answer(text, parse_mode="Markdown")
