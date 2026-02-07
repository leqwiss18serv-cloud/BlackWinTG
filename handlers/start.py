from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
import database
from keyboards.inline import main_menu_kb
import logging

logger = logging.getLogger(__name__)

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Handle /start command"""
    user_id = message.from_user.id
    username = message.from_user.username or f"user_{user_id}"
    
    # Check if user exists
    user = await database.get_user(user_id)
    
    if not user:
        # Create new user
        try:
            user = await database.create_user(user_id, username)
            welcome_text = f"""
🎰 <b>Добро пожаловать в Black Win!</b>

Вы получили <b>10,000 BC</b> для начала игры!

🎮 <b>Доступные игры:</b>
• Удача 50/50 🎲
• Рулетка X3 🎡
• Кости X6 🎯
• Crash X100 🚀
• Монетка X2 🪙
• Колесо X10 🎪
• Слоты 🎰
• Блэкджек 🃏
• Мины 💣
• Башня 🏰
• Plinko ⚪
• Выше/Ниже 📊

💰 <b>Экономика:</b>
• Банк с 5% ежедневным процентом
• Ежедневные бонусы
• Промокоды
• Магазин кейсов

📊 <b>Прогрессия:</b>
• Уровни и опыт (1 BC ставки = 1 XP)
• Достижения
• Лидерборды

Выберите действие из меню ниже:
"""
        except Exception as e:
            logger.error(f"Error creating user {user_id}: {e}")
            await message.answer("❌ Ошибка при регистрации. Попробуйте позже.")
            return
    else:
        # Existing user
        welcome_text = f"""
🎰 <b>С возвращением в Black Win!</b>

💰 Баланс: <b>{user['balance']:,} BC</b>
🏦 В банке: <b>{user['bank_balance']:,} BC</b>
⭐ Уровень: <b>{user['level']}</b>

Выберите действие из меню ниже:
"""
    
    await message.answer(welcome_text, parse_mode="HTML", reply_markup=main_menu_kb())


@router.callback_query(F.data == "main_menu")
async def show_main_menu(callback: CallbackQuery):
    """Show main menu"""
    user_id = callback.from_user.id
    user = await database.get_user(user_id)
    
    if not user:
        await callback.answer("❌ Используйте /start")
        return
    
    text = f"""
🎰 <b>Black Win - Главное меню</b>

💰 Баланс: <b>{user['balance']:,} BC</b>
🏦 В банке: <b>{user['bank_balance']:,} BC</b>
⭐ Уровень: <b>{user['level']}</b>

Выберите действие:
"""
    
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=main_menu_kb())
    await callback.answer()
