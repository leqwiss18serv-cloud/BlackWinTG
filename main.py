import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import config
from keep_alive import keep_alive

# Import handlers
from handlers import start, profile, economy, games, shop, social, admin

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Main function to start the bot"""
    # Initialize bot
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    # Initialize dispatcher
    dp = Dispatcher()
    
    # Register routers
    dp.include_router(start.router)
    dp.include_router(profile.router)
    dp.include_router(economy.router)
    dp.include_router(games.router)
    dp.include_router(shop.router)
    dp.include_router(social.router)
    dp.include_router(admin.router)
    
    logger.info("Bot started successfully!")
    
    # Start polling
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    # Start keep-alive server for Replit
    keep_alive()
    
    # Run bot
    asyncio.run(main())
