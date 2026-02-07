from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
import database
from keyboards.inline import shop_kb, back_to_main_kb
from utils.helpers import format_number
from utils.decorators import not_banned
import random
import logging

logger = logging.getLogger(__name__)

router = Router()


@router.message(Command("shop"))
async def cmd_shop(message: Message):
    """Handle /shop command"""
    await show_shop(message)


@router.callback_query(F.data == "shop")
async def shop_callback(callback: CallbackQuery):
    """Show shop from callback"""
    text = """
🛍️ <b>Магазин кейсов</b>

📦 <b>Обычный кейс</b> - 1,000 BC
Награда: 500-2,000 BC

📦 <b>Редкий кейс</b> - 5,000 BC
Награда: 2,000-15,000 BC

📦 <b>Эпический кейс</b> - 25,000 BC
Награда: 10,000-100,000 BC

📦 <b>Легендарный кейс</b> - 100,000 BC
Награда: 50,000-500,000 BC

Выберите кейс для открытия:
"""
    
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=shop_kb())
    await callback.answer()


async def show_shop(message: Message):
    """Show shop"""
    text = """
🛍️ <b>Магазин кейсов</b>

📦 <b>Обычный кейс</b> - 1,000 BC
Награда: 500-2,000 BC

📦 <b>Редкий кейс</b> - 5,000 BC
Награда: 2,000-15,000 BC

📦 <b>Эпический кейс</b> - 25,000 BC
Награда: 10,000-100,000 BC

📦 <b>Легендарный кейс</b> - 100,000 BC
Награда: 50,000-500,000 BC

Выберите кейс для открытия:
"""
    
    await message.answer(text, parse_mode="HTML", reply_markup=shop_kb())


@router.callback_query(F.data.startswith("case_"))
@not_banned
async def open_case(callback: CallbackQuery):
    """Open a case"""
    case_type = callback.data.split("_")[1]
    
    cases = {
        'common': {'price': 1000, 'min': 500, 'max': 2000, 'name': 'Обычный'},
        'rare': {'price': 5000, 'min': 2000, 'max': 15000, 'name': 'Редкий'},
        'epic': {'price': 25000, 'min': 10000, 'max': 100000, 'name': 'Эпический'},
        'legendary': {'price': 100000, 'min': 50000, 'max': 500000, 'name': 'Легендарный'}
    }
    
    if case_type not in cases:
        await callback.answer("❌ Неизвестный кейс")
        return
    
    case = cases[case_type]
    user = await database.get_user(callback.from_user.id)
    
    if user['balance'] < case['price']:
        await callback.answer(
            f"❌ Недостаточно средств. Нужно: {format_number(case['price'])} BC",
            show_alert=True
        )
        return
    
    # Deduct price
    await database.update_balance(callback.from_user.id, -case['price'], add=True)
    
    # Generate reward
    reward = random.randint(case['min'], case['max'])
    
    # Add reward
    await database.update_balance(callback.from_user.id, reward, add=True)
    
    # Profit/loss
    profit = reward - case['price']
    profit_text = f"+{format_number(profit)}" if profit > 0 else format_number(profit)
    
    text = f"""
📦 <b>{case['name']} кейс открыт!</b>

🎁 Награда: <b>{format_number(reward)} BC</b>
📊 Профит: <b>{profit_text} BC</b>
"""
    
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=shop_kb())
    await callback.answer()
