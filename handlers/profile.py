from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
import database
from keyboards.inline import back_to_main_kb
from utils.helpers import format_number, get_progress_bar, get_xp_for_next_level, calculate_level_xp
import logging

logger = logging.getLogger(__name__)

router = Router()


@router.message(Command("profile"))
async def cmd_profile(message: Message):
    """Handle /profile command"""
    await show_profile(message)


@router.callback_query(F.data == "profile")
async def profile_callback(callback: CallbackQuery):
    """Show profile from callback"""
    await show_profile(callback.message, callback)


async def show_profile(message: Message, callback: CallbackQuery = None):
    """Show user profile"""
    user_id = message.chat.id if callback else message.from_user.id
    user = await database.get_user(user_id)
    
    if not user:
        text = "❌ Используйте /start для регистрации"
        if callback:
            await callback.answer(text)
        else:
            await message.answer(text)
        return
    
    # Calculate XP progress
    current_xp = user['xp']
    current_level = user['level']
    xp_for_current_level = calculate_level_xp(current_level)
    xp_for_next_level = calculate_level_xp(current_level + 1)
    xp_in_current_level = current_xp - xp_for_current_level
    xp_needed = xp_for_next_level - xp_for_current_level
    
    progress = get_progress_bar(xp_in_current_level, xp_needed)
    
    # Calculate win rate
    total_games = user['total_bets']
    wins = user['wins']
    win_rate = (wins / total_games * 100) if total_games > 0 else 0
    
    # Role emoji
    role_emoji = {
        'owner': '👑',
        'admin': '🛡️',
        'user': '👤'
    }
    
    text = f"""
👤 <b>Профиль: {user['username']}</b>
{role_emoji.get(user['role'], '👤')} Роль: <b>{user['role'].title()}</b>

💰 <b>Финансы:</b>
• Баланс: <b>{format_number(user['balance'])} BC</b>
• В банке: <b>{format_number(user['bank_balance'])} BC</b>
• Всего: <b>{format_number(user['balance'] + user['bank_balance'])} BC</b>

⭐ <b>Прогресс:</b>
• Уровень: <b>{current_level}</b>
• Опыт: <b>{format_number(xp_in_current_level)}/{format_number(xp_needed)} XP</b>
{progress}

📊 <b>Статистика:</b>
• Всего ставок: <b>{format_number(total_games)}</b>
• Побед: <b>{format_number(wins)}</b>
• Винрейт: <b>{win_rate:.1f}%</b>
• Выиграно: <b>{format_number(user['total_won'])} BC</b>
• Проиграно: <b>{format_number(user['total_lost'])} BC</b>
• Профит: <b>{format_number(user['total_won'] - user['total_lost'])} BC</b>
"""
    
    if callback:
        await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_to_main_kb())
        await callback.answer()
    else:
        await message.answer(text, parse_mode="HTML", reply_markup=back_to_main_kb())


@router.callback_query(F.data == "balance")
async def balance_callback(callback: CallbackQuery):
    """Show balance"""
    user = await database.get_user(callback.from_user.id)
    
    if not user:
        await callback.answer("❌ Используйте /start")
        return
    
    text = f"""
💰 <b>Ваш баланс</b>

💵 Кошелёк: <b>{format_number(user['balance'])} BC</b>
🏦 Банк: <b>{format_number(user['bank_balance'])} BC</b>
💎 Всего: <b>{format_number(user['balance'] + user['bank_balance'])} BC</b>

<i>Храните BC в банке и получайте 5% ежедневно!</i>
"""
    
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_to_main_kb())
    await callback.answer()
