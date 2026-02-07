from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
import database
from keyboards.inline import back_to_main_kb
from utils.helpers import format_number, get_rank_emoji
import logging

logger = logging.getLogger(__name__)

router = Router()


@router.message(Command("friends"))
async def cmd_friends(message: Message):
    """Handle /friends command"""
    await message.answer(
        "👥 <b>Друзья</b>\n\n🚧 Система друзей скоро будет доступна!",
        parse_mode="HTML",
        reply_markup=back_to_main_kb()
    )


@router.callback_query(F.data == "friends")
async def friends_callback(callback: CallbackQuery):
    """Show friends from callback"""
    await callback.message.edit_text(
        "👥 <b>Друзья</b>\n\n🚧 Система друзей скоро будет доступна!",
        parse_mode="HTML",
        reply_markup=back_to_main_kb()
    )
    await callback.answer()


@router.message(Command("top"))
async def cmd_top(message: Message):
    """Handle /top command"""
    await show_leaderboard(message)


@router.callback_query(F.data == "leaderboard")
async def leaderboard_callback(callback: CallbackQuery):
    """Show leaderboard from callback"""
    await show_leaderboard(callback.message, callback)


async def show_leaderboard(message: Message, callback: CallbackQuery = None):
    """Show leaderboard"""
    # Get top by balance
    top_balance = await database.get_top_balance(10)
    
    # Get top by level
    top_level = await database.get_top_level(10)
    
    text = "🏆 <b>Лидерборд</b>\n\n"
    
    # Top by balance
    text += "💰 <b>По балансу:</b>\n"
    for i, user in enumerate(top_balance, 1):
        emoji = get_rank_emoji(i)
        text += f"{emoji} {user['username']}: {format_number(user['balance'])} BC\n"
    
    text += "\n⭐ <b>По уровню:</b>\n"
    for i, user in enumerate(top_level, 1):
        emoji = get_rank_emoji(i)
        text += f"{emoji} {user['username']}: Ур.{user['level']} ({format_number(user['xp'])} XP)\n"
    
    if callback:
        await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_to_main_kb())
        await callback.answer()
    else:
        await message.answer(text, parse_mode="HTML", reply_markup=back_to_main_kb())
