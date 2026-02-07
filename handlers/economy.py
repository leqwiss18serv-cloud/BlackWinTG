from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import database
from keyboards.inline import bank_kb, back_to_main_kb
from utils.helpers import format_number, get_random_daily_bonus
from utils.decorators import not_banned
import logging

logger = logging.getLogger(__name__)

router = Router()


class BankStates(StatesGroup):
    waiting_for_deposit = State()
    waiting_for_withdraw = State()


@router.message(Command("bank"))
async def cmd_bank(message: Message):
    """Handle /bank command"""
    await show_bank(message)


@router.callback_query(F.data == "bank")
async def bank_callback(callback: CallbackQuery):
    """Show bank from callback"""
    user = await database.get_user(callback.from_user.id)
    
    if not user:
        await callback.answer("❌ Используйте /start")
        return
    
    text = f"""
🏦 <b>Black Win Bank</b>

💰 Баланс кошелька: <b>{format_number(user['balance'])} BC</b>
🏦 Баланс в банке: <b>{format_number(user['bank_balance'])} BC</b>

📈 <b>Процентная ставка: 5% ежедневно</b>

<i>Храните BC в банке и получайте пассивный доход!</i>

Выберите действие:
"""
    
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=bank_kb())
    await callback.answer()


async def show_bank(message: Message):
    """Show bank"""
    user = await database.get_user(message.from_user.id)
    
    if not user:
        await message.answer("❌ Используйте /start")
        return
    
    text = f"""
🏦 <b>Black Win Bank</b>

💰 Баланс кошелька: <b>{format_number(user['balance'])} BC</b>
🏦 Баланс в банке: <b>{format_number(user['bank_balance'])} BC</b>

📈 <b>Процентная ставка: 5% ежедневно</b>

<i>Храните BC в банке и получайте пассивный доход!</i>

Выберите действие:
"""
    
    await message.answer(text, parse_mode="HTML", reply_markup=bank_kb())


@router.callback_query(F.data == "bank_deposit")
async def bank_deposit_start(callback: CallbackQuery, state: FSMContext):
    """Start bank deposit"""
    user = await database.get_user(callback.from_user.id)
    
    text = f"""
💵 <b>Внести в банк</b>

Ваш баланс: <b>{format_number(user['balance'])} BC</b>

Введите сумму для внесения:
"""
    
    await callback.message.edit_text(text, parse_mode="HTML")
    await state.set_state(BankStates.waiting_for_deposit)
    await callback.answer()


@router.message(BankStates.waiting_for_deposit)
@not_banned
async def bank_deposit_process(message: Message, state: FSMContext):
    """Process bank deposit"""
    try:
        amount = int(message.text)
        
        if amount <= 0:
            await message.answer("❌ Сумма должна быть положительной")
            return
        
        user = await database.get_user(message.from_user.id)
        
        if amount > user['balance']:
            await message.answer(f"❌ Недостаточно средств. Ваш баланс: {format_number(user['balance'])} BC")
            return
        
        # Deposit
        success = await database.deposit_to_bank(message.from_user.id, amount)
        
        if success:
            await message.answer(
                f"✅ Успешно внесено {format_number(amount)} BC в банк!",
                reply_markup=back_to_main_kb()
            )
        else:
            await message.answer("❌ Ошибка при внесении средств")
        
        await state.clear()
    except ValueError:
        await message.answer("❌ Введите корректное число")


@router.callback_query(F.data == "bank_withdraw")
async def bank_withdraw_start(callback: CallbackQuery, state: FSMContext):
    """Start bank withdrawal"""
    user = await database.get_user(callback.from_user.id)
    
    text = f"""
💸 <b>Снять с банка</b>

В банке: <b>{format_number(user['bank_balance'])} BC</b>

Введите сумму для снятия:
"""
    
    await callback.message.edit_text(text, parse_mode="HTML")
    await state.set_state(BankStates.waiting_for_withdraw)
    await callback.answer()


@router.message(BankStates.waiting_for_withdraw)
@not_banned
async def bank_withdraw_process(message: Message, state: FSMContext):
    """Process bank withdrawal"""
    try:
        amount = int(message.text)
        
        if amount <= 0:
            await message.answer("❌ Сумма должна быть положительной")
            return
        
        user = await database.get_user(message.from_user.id)
        
        if amount > user['bank_balance']:
            await message.answer(f"❌ Недостаточно средств в банке. Доступно: {format_number(user['bank_balance'])} BC")
            return
        
        # Withdraw
        success = await database.withdraw_from_bank(message.from_user.id, amount)
        
        if success:
            await message.answer(
                f"✅ Успешно снято {format_number(amount)} BC с банка!",
                reply_markup=back_to_main_kb()
            )
        else:
            await message.answer("❌ Ошибка при снятии средств")
        
        await state.clear()
    except ValueError:
        await message.answer("❌ Введите корректное число")


# Daily bonus
@router.message(Command("daily"))
async def cmd_daily(message: Message):
    """Handle /daily command"""
    await claim_daily(message)


@router.callback_query(F.data == "daily")
async def daily_callback(callback: CallbackQuery):
    """Claim daily bonus from callback"""
    await claim_daily(callback.message, callback)


async def claim_daily(message: Message, callback: CallbackQuery = None):
    """Claim daily bonus"""
    user_id = message.chat.id if callback else message.from_user.id
    
    # Check if can claim
    can_claim = await database.can_claim_daily(user_id)
    
    if not can_claim:
        text = "⏰ Ежедневный бонус уже получен!\n\nПриходите завтра!"
        if callback:
            await callback.answer(text, show_alert=True)
        else:
            await message.answer(text)
        return
    
    # Get random bonus
    bonus = get_random_daily_bonus()
    
    # Check for x2 daily event
    events = await database.get_active_events()
    for event in events:
        if event['type'] == 'x2daily':
            bonus *= 2
            break
    
    # Add balance
    await database.update_balance(user_id, bonus, add=True)
    await database.update_daily_bonus(user_id)
    
    text = f"🎁 Ежедневный бонус получен!\n\n+{format_number(bonus)} BC"
    
    if callback:
        await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_to_main_kb())
        await callback.answer()
    else:
        await message.answer(text, parse_mode="HTML", reply_markup=back_to_main_kb())


# Promo codes
@router.message(Command("promo"))
async def cmd_promo(message: Message):
    """Handle /promo command"""
    args = message.text.split()
    
    if len(args) < 2:
        await message.answer("❌ Использование: /promo <код>")
        return
    
    code = args[1]
    success, msg = await database.use_promo(message.from_user.id, code)
    
    await message.answer(msg)
