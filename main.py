import asyncio
import logging
import sys
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


def check_config():
    """Check if all required environment variables are set"""
    errors = []
    
    if not config.BOT_TOKEN:
        errors.append("BOT_TOKEN")
    if not config.SUPABASE_URL:
        errors.append("SUPABASE_URL")
    if not config.SUPABASE_KEY:
        errors.append("SUPABASE_KEY")
    
    if errors:
        logger.error(f"Missing required environment variables: {', '.join(errors)}")
        logger.error("Please set them in Replit Secrets or .env file")
        sys.exit(1)


async def main():
    """Main function to start the bot"""
    # Check configuration
    check_config()
    
    # Initialize bot
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    # Delete webhook before starting polling (fixes conflict error)
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Webhook deleted, starting polling...")
    
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
