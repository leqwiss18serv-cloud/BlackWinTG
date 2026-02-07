from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import database
from keyboards.inline import admin_kb, events_kb, back_to_main_kb
from utils.helpers import format_number
from utils.decorators import owner_only, admin_only
import logging

logger = logging.getLogger(__name__)

router = Router()


class AdminStates(StatesGroup):
    waiting_for_broadcast = State()
    waiting_for_event_duration = State()


@router.message(Command("admin"))
@admin_only
async def cmd_admin(message: Message):
    """Handle /admin command"""
    text = """
🛡️ <b>Панель администратора</b>

Выберите действие:
"""
    
    await message.answer(text, parse_mode="HTML", reply_markup=admin_kb())


@router.callback_query(F.data == "admin")
async def admin_callback(callback: CallbackQuery):
    """Show admin panel from callback"""
    user = await database.get_user(callback.from_user.id)
    
    if not user or user['role'] not in ['admin', 'owner']:
        await callback.answer("⛔ Доступ запрещён", show_alert=True)
        return
    
    text = """
🛡️ <b>Панель администратора</b>

Выберите действие:
"""
    
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=admin_kb())
    await callback.answer()


@router.callback_query(F.data == "admin_stats")
async def admin_stats(callback: CallbackQuery):
    """Show bot statistics"""
    user = await database.get_user(callback.from_user.id)
    
    if not user or user['role'] not in ['admin', 'owner']:
        await callback.answer("⛔ Доступ запрещён", show_alert=True)
        return
    
    stats = await database.get_bot_stats()
    
    text = f"""
📊 <b>Статистика бота</b>

👥 Всего пользователей: <b>{stats.get('total_users', 0)}</b>
🎲 Всего ставок: <b>{format_number(stats.get('total_bets', 0))}</b>
💰 Выиграно: <b>{format_number(stats.get('total_won', 0))} BC</b>
💸 Проиграно: <b>{format_number(stats.get('total_lost', 0))} BC</b>
"""
    
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=admin_kb())
    await callback.answer()


@router.callback_query(F.data == "admin_broadcast")
async def admin_broadcast_start(callback: CallbackQuery, state: FSMContext):
    """Start broadcast"""
    user = await database.get_user(callback.from_user.id)
    
    if not user or user['role'] != 'owner':
        await callback.answer("⛔ Только для владельца", show_alert=True)
        return
    
    text = """
📢 <b>Рассылка</b>

Введите текст для рассылки всем пользователям:
"""
    
    await callback.message.edit_text(text, parse_mode="HTML")
    await state.set_state(AdminStates.waiting_for_broadcast)
    await callback.answer()


@router.message(AdminStates.waiting_for_broadcast)
@owner_only
async def admin_broadcast_send(message: Message, state: FSMContext):
    """Send broadcast"""
    text = message.text
    
    # Get all user IDs
    user_ids = await database.get_all_user_ids()
    
    success_count = 0
    fail_count = 0
    
    await message.answer(f"📤 Отправка рассылки {len(user_ids)} пользователям...")
    
    for user_id in user_ids:
        try:
            await message.bot.send_message(user_id, text)
            success_count += 1
        except Exception as e:
            logger.error(f"Failed to send broadcast to {user_id}: {e}")
            fail_count += 1
    
    await message.answer(
        f"✅ Рассылка завершена!\n\nУспешно: {success_count}\nОшибок: {fail_count}",
        reply_markup=admin_kb()
    )
    await state.clear()


@router.callback_query(F.data == "admin_events")
async def admin_events(callback: CallbackQuery):
    """Show events menu"""
    user = await database.get_user(callback.from_user.id)
    
    if not user or user['role'] not in ['admin', 'owner']:
        await callback.answer("⛔ Доступ запрещён", show_alert=True)
        return
    
    # Get active events
    active_events = await database.get_active_events()
    
    text = "🎉 <b>Ивенты</b>\n\n"
    
    if active_events:
        text += "<b>Активные ивенты:</b>\n"
        for event in active_events:
            event_names = {
                'x2xp': '✨ x2 XP',
                'x2win': '💰 x2 WIN',
                'x2daily': '🎁 x2 DAILY'
            }
            text += f"{event_names.get(event['type'], event['type'])}\n"
    else:
        text += "Нет активных ивентов\n"
    
    text += "\nВыберите ивент для запуска:"
    
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=events_kb())
    await callback.answer()


@router.callback_query(F.data.startswith("event_"))
async def admin_event_start(callback: CallbackQuery, state: FSMContext):
    """Start event"""
    user = await database.get_user(callback.from_user.id)
    
    if not user or user['role'] not in ['admin', 'owner']:
        await callback.answer("⛔ Доступ запрещён", show_alert=True)
        return
    
    event_type = callback.data.split("_")[1]
    
    text = f"""
🎉 <b>Запуск ивента</b>

Введите длительность в минутах:
"""
    
    await callback.message.edit_text(text, parse_mode="HTML")
    await state.set_state(AdminStates.waiting_for_event_duration)
    await state.update_data(event_type=event_type)
    await callback.answer()


@router.message(AdminStates.waiting_for_event_duration)
async def admin_event_create(message: Message, state: FSMContext):
    """Create event"""
    user = await database.get_user(message.from_user.id)
    
    if not user or user['role'] not in ['admin', 'owner']:
        await message.answer("⛔ Доступ запрещён")
        return
    
    try:
        duration = int(message.text)
        
        if duration <= 0 or duration > 1440:  # Max 24 hours
            await message.answer("❌ Длительность должна быть от 1 до 1440 минут")
            return
        
        data = await state.get_data()
        event_type = data.get('event_type')
        
        # Create event
        success = await database.create_event(event_type, duration, message.from_user.id)
        
        if success:
            event_names = {
                'x2xp': '✨ x2 XP',
                'x2win': '💰 x2 WIN',
                'x2daily': '🎁 x2 DAILY'
            }
            
            await message.answer(
                f"✅ Ивент {event_names.get(event_type, event_type)} запущен на {duration} минут!",
                reply_markup=admin_kb()
            )
            
            # Broadcast to all users
            user_ids = await database.get_all_user_ids()
            broadcast_text = f"🎉 <b>Ивент запущен!</b>\n\n{event_names.get(event_type, event_type)} активен {duration} минут!"
            
            for user_id in user_ids:
                try:
                    await message.bot.send_message(user_id, broadcast_text, parse_mode="HTML")
                except Exception:
                    pass
        else:
            await message.answer("❌ Ошибка создания ивента")
        
        await state.clear()
        
    except ValueError:
        await message.answer("❌ Введите корректное число")


# Owner commands
@router.message(Command("ban"))
@owner_only
async def cmd_ban(message: Message):
    """Ban user"""
    args = message.text.split(maxsplit=2)
    
    if len(args) < 3:
        await message.answer("❌ Использование: /ban <user_id> <причина>")
        return
    
    try:
        user_id = int(args[1])
        reason = args[2]
        
        success = await database.ban_user(user_id, reason)
        
        if success:
            await message.answer(f"✅ Пользователь {user_id} заблокирован")
        else:
            await message.answer("❌ Ошибка блокировки")
    except ValueError:
        await message.answer("❌ Неверный ID пользователя")


@router.message(Command("unban"))
@owner_only
async def cmd_unban(message: Message):
    """Unban user"""
    args = message.text.split()
    
    if len(args) < 2:
        await message.answer("❌ Использование: /unban <user_id>")
        return
    
    try:
        user_id = int(args[1])
        
        success = await database.unban_user(user_id)
        
        if success:
            await message.answer(f"✅ Пользователь {user_id} разблокирован")
        else:
            await message.answer("❌ Ошибка разблокировки")
    except ValueError:
        await message.answer("❌ Неверный ID пользователя")


@router.message(Command("addbal"))
@owner_only
async def cmd_addbal(message: Message):
    """Add balance to user"""
    args = message.text.split()
    
    if len(args) < 3:
        await message.answer("❌ Использование: /addbal <user_id> <сумма>")
        return
    
    try:
        user_id = int(args[1])
        amount = int(args[2])
        
        success = await database.update_balance(user_id, amount, add=True)
        
        if success:
            await message.answer(f"✅ Добавлено {format_number(amount)} BC пользователю {user_id}")
        else:
            await message.answer("❌ Ошибка")
    except ValueError:
        await message.answer("❌ Неверные аргументы")


@router.message(Command("setbal"))
@owner_only
async def cmd_setbal(message: Message):
    """Set balance for user"""
    args = message.text.split()
    
    if len(args) < 3:
        await message.answer("❌ Использование: /setbal <user_id> <сумма>")
        return
    
    try:
        user_id = int(args[1])
        amount = int(args[2])
        
        success = await database.update_balance(user_id, amount, add=False)
        
        if success:
            await message.answer(f"✅ Баланс {user_id} установлен на {format_number(amount)} BC")
        else:
            await message.answer("❌ Ошибка")
    except ValueError:
        await message.answer("❌ Неверные аргументы")


@router.message(Command("addadmin"))
@owner_only
async def cmd_addadmin(message: Message):
    """Add admin"""
    args = message.text.split()
    
    if len(args) < 2:
        await message.answer("❌ Использование: /addadmin <user_id>")
        return
    
    try:
        user_id = int(args[1])
        
        success = await database.set_role(user_id, 'admin')
        
        if success:
            await message.answer(f"✅ Пользователь {user_id} назначен администратором")
        else:
            await message.answer("❌ Ошибка")
    except ValueError:
        await message.answer("❌ Неверный ID пользователя")


@router.message(Command("removeadmin"))
@owner_only
async def cmd_removeadmin(message: Message):
    """Remove admin"""
    args = message.text.split()
    
    if len(args) < 2:
        await message.answer("❌ Использование: /removeadmin <user_id>")
        return
    
    try:
        user_id = int(args[1])
        
        success = await database.set_role(user_id, 'user')
        
        if success:
            await message.answer(f"✅ Пользователь {user_id} снят с поста администратора")
        else:
            await message.answer("❌ Ошибка")
    except ValueError:
        await message.answer("❌ Неверный ID пользователя")


@router.message(Command("createpromo"))
@owner_only
async def cmd_createpromo(message: Message):
    """Create promo code"""
    args = message.text.split()
    
    if len(args) < 4:
        await message.answer("❌ Использование: /createpromo <код> <сумма> <использований>")
        return
    
    try:
        code = args[1]
        amount = int(args[2])
        max_uses = int(args[3])
        
        success = await database.create_promo(code, amount, max_uses, message.from_user.id)
        
        if success:
            await message.answer(f"✅ Промокод '{code}' создан\n\nСумма: {format_number(amount)} BC\nИспользований: {max_uses}")
        else:
            await message.answer("❌ Ошибка создания промокода")
    except ValueError:
        await message.answer("❌ Неверные аргументы")


@router.message(Command("stats"))
@owner_only
async def cmd_stats(message: Message):
    """Show bot statistics"""
    stats = await database.get_bot_stats()
    
    text = f"""
📊 <b>Статистика бота</b>

👥 Всего пользователей: <b>{stats.get('total_users', 0)}</b>
🎲 Всего ставок: <b>{format_number(stats.get('total_bets', 0))}</b>
💰 Выиграно: <b>{format_number(stats.get('total_won', 0))} BC</b>
💸 Проиграно: <b>{format_number(stats.get('total_lost', 0))} BC</b>
"""
    
    await message.answer(text, parse_mode="HTML")


@router.callback_query(F.data == "admin_users")
async def admin_users(callback: CallbackQuery):
    """Manage users (placeholder)"""
    await callback.answer("🚧 Управление пользователями скоро будет доступно!", show_alert=True)


@router.callback_query(F.data == "admin_promos")
async def admin_promos(callback: CallbackQuery):
    """Manage promos (placeholder)"""
    await callback.answer("🚧 Управление промокодами через /createpromo", show_alert=True)
