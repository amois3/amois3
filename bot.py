"""Main bot application."""
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config import settings
from database.mongodb import db
from handlers import routers

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger(__name__)


async def main():
    """Run bot."""
    # Log token for debugging
    token = settings.telegram_bot_token
    logger.info(f"Using token: {token[:10]}...{token[-4:]}")

    # Initialize bot and dispatcher
    bot = Bot(token=token, parse_mode=ParseMode.MARKDOWN)
    dp = Dispatcher()

    # Register all routers
    for router in routers:
        dp.include_router(router)

    # Connect to database
    await db.connect()

    # Start polling
    logger.info("Bot starting...")
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await db.disconnect()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
