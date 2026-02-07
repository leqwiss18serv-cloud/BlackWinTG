from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import database
from keyboards.inline import (
    games_menu_kb, back_to_games_kb, coin_flip_kb,
    roulette_kb, dice_kb, blackjack_kb
)
from utils.helpers import (
    format_number, play_dice_game, play_coin_flip,
    play_5050, play_roulette, play_wheel, play_slots,
    play_crash, play_plinko, calculate_blackjack_score, get_card
)
from utils.decorators import not_banned
import config
import random
import logging

logger = logging.getLogger(__name__)

router = Router()


class GameStates(StatesGroup):
    waiting_for_bet = State()
    waiting_for_crash_cashout = State()
    blackjack_playing = State()


# Games menu
@router.message(Command("games"))
async def cmd_games(message: Message):
    """Handle /games command"""
    await show_games_menu(message)


@router.callback_query(F.data == "games")
async def games_callback(callback: CallbackQuery, state: FSMContext):
    """Show games menu from callback"""
    await state.clear()  # Clear any active game state
    
    text = """
🎮 <b>Black Win - Игры</b>

Выберите игру:

🎲 <b>Удача 50/50</b> - шанс 50%, выигрыш x2
🎡 <b>Рулетка X3</b> - красное/чёрное/зелёное, выигрыш x3
🎯 <b>Кости X6</b> - угадать 1-6, выигрыш x6
🚀 <b>Crash X100</b> - множитель до x100
🪙 <b>Монетка X2</b> - орёл/решка, выигрыш x2
🎪 <b>Колесо X10</b> - шанс 10%, выигрыш x10
🎰 <b>Слоты</b> - 3 символа, до x50
🃏 <b>Блэкджек</b> - классическая игра 21
💣 <b>Мины</b> - найти алмазы (скоро)
🏰 <b>Башня</b> - 10 этажей (скоро)
⚪ <b>Plinko</b> - падающий шар, до x50
📊 <b>Выше/Ниже</b> - угадать число (скоро)

💰 <b>Джекпот</b> - общий банк (скоро)
⚔️ <b>Дуэли</b> - PvP ставки (скоро)
"""
    
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=games_menu_kb())
    await callback.answer()


async def show_games_menu(message: Message):
    """Show games menu"""
    text = """
🎮 <b>Black Win - Игры</b>

Выберите игру:

🎲 <b>Удача 50/50</b> - шанс 50%, выигрыш x2
🎡 <b>Рулетка X3</b> - красное/чёрное/зелёное, выигрыш x3
🎯 <b>Кости X6</b> - угадать 1-6, выигрыш x6
🚀 <b>Crash X100</b> - множитель до x100
🪙 <b>Монетка X2</b> - орёл/решка, выигрыш x2
🎪 <b>Колесо X10</b> - шанс 10%, выигрыш x10
🎰 <b>Слоты</b> - 3 символа, до x50
🃏 <b>Блэкджек</b> - классическая игра 21
⚪ <b>Plinko</b> - падающий шар, до x50
"""
    
    await message.answer(text, parse_mode="HTML", reply_markup=games_menu_kb())


# 50/50 Game
@router.callback_query(F.data == "game_5050")
async def game_5050_start(callback: CallbackQuery, state: FSMContext):
    """Start 50/50 game"""
    text = """
🎲 <b>Удача 50/50</b>

Шанс выигрыша: 50%
Множитель: x2

Введите сумму ставки:
"""
    
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_to_games_kb())
    await state.set_state(GameStates.waiting_for_bet)
    await state.update_data(game="5050")
    await callback.answer()


# Coin Flip Game
@router.callback_query(F.data == "game_coin")
async def game_coin_start(callback: CallbackQuery, state: FSMContext):
    """Start coin flip game"""
    text = """
🪙 <b>Монетка</b>

Шанс выигрыша: 50%
Множитель: x2

Введите сумму ставки:
"""
    
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_to_games_kb())
    await state.set_state(GameStates.waiting_for_bet)
    await state.update_data(game="coin")
    await callback.answer()


@router.callback_query(F.data.startswith("coin_"))
async def coin_choice(callback: CallbackQuery, state: FSMContext):
    """Handle coin choice"""
    choice = callback.data.split("_")[1]  # heads or tails
    data = await state.get_data()
    bet = data.get('bet', 0)
    
    user = await database.get_user(callback.from_user.id)
    
    # Play game
    won, result, win_amount = play_coin_flip(bet, choice)
    
    # Apply event multiplier
    if won:
        events = await database.get_active_events()
        for event in events:
            if event['type'] == 'x2win':
                win_amount *= 2
                break
    
    # Update balance
    if won:
        await database.update_balance(callback.from_user.id, win_amount, add=True)
    
    # Add XP
    xp_data = await database.add_xp(callback.from_user.id, bet * config.XP_PER_BC)
    
    # Record bet
    await database.record_bet(callback.from_user.id, bet, won, win_amount)
    
    # Result
    result_emoji = "🦅" if result == "heads" else "🌟"
    choice_emoji = "🦅" if choice == "heads" else "🌟"
    
    if won:
        text = f"""
✅ <b>Победа!</b>

Ваш выбор: {choice_emoji}
Результат: {result_emoji}

Выигрыш: <b>+{format_number(win_amount)} BC</b>
"""
    else:
        text = f"""
❌ <b>Проигрыш</b>

Ваш выбор: {choice_emoji}
Результат: {result_emoji}

Потеряно: <b>-{format_number(bet)} BC</b>
"""
    
    if xp_data.get('leveled_up'):
        text += f"\n🎉 <b>Новый уровень {xp_data['new_level']}!</b>"
    
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_to_games_kb())
    await state.clear()
    await callback.answer()


# Roulette Game
@router.callback_query(F.data == "game_roulette")
async def game_roulette_start(callback: CallbackQuery, state: FSMContext):
    """Start roulette game"""
    text = """
🎡 <b>Рулетка X3</b>

Шанс выигрыша: 33% (каждый цвет)
Множитель: x3

Введите сумму ставки:
"""
    
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_to_games_kb())
    await state.set_state(GameStates.waiting_for_bet)
    await state.update_data(game="roulette")
    await callback.answer()


@router.callback_query(F.data.startswith("roulette_"))
async def roulette_choice(callback: CallbackQuery, state: FSMContext):
    """Handle roulette choice"""
    choice = callback.data.split("_")[1]  # red, black, or green
    data = await state.get_data()
    bet = data.get('bet', 0)
    
    # Play game
    won, result, win_amount = play_roulette(bet, choice)
    
    # Apply event multiplier
    if won:
        events = await database.get_active_events()
        for event in events:
            if event['type'] == 'x2win':
                win_amount *= 2
                break
    
    # Update balance
    if won:
        await database.update_balance(callback.from_user.id, win_amount, add=True)
    
    # Add XP
    xp_data = await database.add_xp(callback.from_user.id, bet * config.XP_PER_BC)
    
    # Record bet
    await database.record_bet(callback.from_user.id, bet, won, win_amount)
    
    # Result
    result_emoji = {"red": "🔴", "black": "⚫", "green": "🟢"}
    choice_emoji = result_emoji.get(choice, "")
    result_emoji_show = result_emoji.get(result, "")
    
    if won:
        text = f"""
✅ <b>Победа!</b>

Ваш выбор: {choice_emoji}
Результат: {result_emoji_show}

Выигрыш: <b>+{format_number(win_amount)} BC</b>
"""
    else:
        text = f"""
❌ <b>Проигрыш</b>

Ваш выбор: {choice_emoji}
Результат: {result_emoji_show}

Потеряно: <b>-{format_number(bet)} BC</b>
"""
    
    if xp_data.get('leveled_up'):
        text += f"\n🎉 <b>Новый уровень {xp_data['new_level']}!</b>"
    
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_to_games_kb())
    await state.clear()
    await callback.answer()


# Dice Game
@router.callback_query(F.data == "game_dice")
async def game_dice_start(callback: CallbackQuery, state: FSMContext):
    """Start dice game"""
    text = """
🎯 <b>Кости X6</b>

Шанс выигрыша: 16.7%
Множитель: x6

Введите сумму ставки:
"""
    
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_to_games_kb())
    await state.set_state(GameStates.waiting_for_bet)
    await state.update_data(game="dice")
    await callback.answer()


@router.callback_query(F.data.startswith("dice_"))
async def dice_choice(callback: CallbackQuery, state: FSMContext):
    """Handle dice choice"""
    choice = int(callback.data.split("_")[1])
    data = await state.get_data()
    bet = data.get('bet', 0)
    
    # Play game
    won, roll, win_amount = play_dice_game(bet, choice)
    
    # Apply event multiplier
    if won:
        events = await database.get_active_events()
        for event in events:
            if event['type'] == 'x2win':
                win_amount *= 2
                break
    
    # Update balance
    if won:
        await database.update_balance(callback.from_user.id, win_amount, add=True)
    
    # Add XP
    xp_data = await database.add_xp(callback.from_user.id, bet * config.XP_PER_BC)
    
    # Record bet
    await database.record_bet(callback.from_user.id, bet, won, win_amount)
    
    if won:
        text = f"""
✅ <b>Победа!</b>

Ваш выбор: {choice}
Выпало: {roll}

Выигрыш: <b>+{format_number(win_amount)} BC</b>
"""
    else:
        text = f"""
❌ <b>Проигрыш</b>

Ваш выбор: {choice}
Выпало: {roll}

Потеряно: <b>-{format_number(bet)} BC</b>
"""
    
    if xp_data.get('leveled_up'):
        text += f"\n🎉 <b>Новый уровень {xp_data['new_level']}!</b>"
    
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_to_games_kb())
    await state.clear()
    await callback.answer()


# Wheel Game
@router.callback_query(F.data == "game_wheel")
async def game_wheel_start(callback: CallbackQuery, state: FSMContext):
    """Start wheel game"""
    text = """
🎪 <b>Колесо X10</b>

Шанс выигрыша: 10%
Множитель: x10

Введите сумму ставки:
"""
    
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_to_games_kb())
    await state.set_state(GameStates.waiting_for_bet)
    await state.update_data(game="wheel")
    await callback.answer()


# Slots Game
@router.callback_query(F.data == "game_slots")
async def game_slots_start(callback: CallbackQuery, state: FSMContext):
    """Start slots game"""
    text = """
🎰 <b>Слоты</b>

Множители:
🍒🍒🍒 - x5
🍋🍋🍋 - x10
🍊🍊🍊 - x15
🍇🍇🍇 - x20
💎💎💎 - x30
7️⃣7️⃣7️⃣ - x50

Введите сумму ставки:
"""
    
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_to_games_kb())
    await state.set_state(GameStates.waiting_for_bet)
    await state.update_data(game="slots")
    await callback.answer()


# Plinko Game
@router.callback_query(F.data == "game_plinko")
async def game_plinko_start(callback: CallbackQuery, state: FSMContext):
    """Start plinko game"""
    text = """
⚪ <b>Plinko</b>

Шар падает через колышки
Множители: x1 - x50

Введите сумму ставки:
"""
    
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_to_games_kb())
    await state.set_state(GameStates.waiting_for_bet)
    await state.update_data(game="plinko")
    await callback.answer()


# Crash Game
@router.callback_query(F.data == "game_crash")
async def game_crash_start(callback: CallbackQuery, state: FSMContext):
    """Start crash game"""
    text = """
🚀 <b>Crash X100</b>

Множитель растёт до краша
Заберите в нужный момент!

Введите сумму ставки:
"""
    
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_to_games_kb())
    await state.set_state(GameStates.waiting_for_bet)
    await state.update_data(game="crash")
    await callback.answer()


# Blackjack Game
@router.callback_query(F.data == "game_blackjack")
async def game_blackjack_start(callback: CallbackQuery, state: FSMContext):
    """Start blackjack game"""
    text = """
🃏 <b>Блэкджек</b>

Наберите 21 или близко к этому
Множитель: x2

Введите сумму ставки:
"""
    
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_to_games_kb())
    await state.set_state(GameStates.waiting_for_bet)
    await state.update_data(game="blackjack")
    await callback.answer()


# Process bet input
@router.message(GameStates.waiting_for_bet)
@not_banned
async def process_bet(message: Message, state: FSMContext):
    """Process bet amount"""
    try:
        bet = int(message.text)
        
        if bet < config.GAME_MIN_BET:
            await message.answer(f"❌ Минимальная ставка: {format_number(config.GAME_MIN_BET)} BC")
            return
        
        if bet > config.GAME_MAX_BET:
            await message.answer(f"❌ Максимальная ставка: {format_number(config.GAME_MAX_BET)} BC")
            return
        
        user = await database.get_user(message.from_user.id)
        
        if bet > user['balance']:
            await message.answer(f"❌ Недостаточно средств. Ваш баланс: {format_number(user['balance'])} BC")
            return
        
        # Deduct bet from balance
        await database.update_balance(message.from_user.id, -bet, add=True)
        
        data = await state.get_data()
        game = data.get('game')
        
        # Route to specific game
        if game == "5050":
            await play_5050_game(message, state, bet)
        elif game == "coin":
            await play_coin_game(message, state, bet)
        elif game == "roulette":
            await play_roulette_game(message, state, bet)
        elif game == "dice":
            await play_dice_game_handler(message, state, bet)
        elif game == "wheel":
            await play_wheel_game(message, state, bet)
        elif game == "slots":
            await play_slots_game(message, state, bet)
        elif game == "plinko":
            await play_plinko_game(message, state, bet)
        elif game == "crash":
            await play_crash_game(message, state, bet)
        elif game == "blackjack":
            await play_blackjack_game(message, state, bet)
        
    except ValueError:
        await message.answer("❌ Введите корректное число")


async def play_5050_game(message: Message, state: FSMContext, bet: int):
    """Play 50/50 game"""
    won, win_amount = play_5050(bet)
    
    # Apply event multiplier
    if won:
        events = await database.get_active_events()
        for event in events:
            if event['type'] == 'x2win':
                win_amount *= 2
                break
    
    # Update balance
    if won:
        await database.update_balance(message.from_user.id, win_amount, add=True)
    
    # Add XP
    xp_data = await database.add_xp(message.from_user.id, bet * config.XP_PER_BC)
    
    # Record bet
    await database.record_bet(message.from_user.id, bet, won, win_amount)
    
    if won:
        text = f"✅ <b>Победа!</b>\n\nВыигрыш: <b>+{format_number(win_amount)} BC</b>"
    else:
        text = f"❌ <b>Проигрыш</b>\n\nПотеряно: <b>-{format_number(bet)} BC</b>"
    
    if xp_data.get('leveled_up'):
        text += f"\n🎉 <b>Новый уровень {xp_data['new_level']}!</b>"
    
    await message.answer(text, parse_mode="HTML", reply_markup=back_to_games_kb())
    await state.clear()


async def play_coin_game(message: Message, state: FSMContext, bet: int):
    """Play coin flip game - show choice"""
    await state.update_data(bet=bet)
    await message.answer("🪙 Выберите сторону:", reply_markup=coin_flip_kb())


async def play_roulette_game(message: Message, state: FSMContext, bet: int):
    """Play roulette game - show choice"""
    await state.update_data(bet=bet)
    await message.answer("🎡 Выберите цвет:", reply_markup=roulette_kb())


async def play_dice_game_handler(message: Message, state: FSMContext, bet: int):
    """Play dice game - show choice"""
    await state.update_data(bet=bet)
    await message.answer("🎯 Выберите число:", reply_markup=dice_kb())


async def play_wheel_game(message: Message, state: FSMContext, bet: int):
    """Play wheel game"""
    won, win_amount = play_wheel(bet)
    
    # Apply event multiplier
    if won:
        events = await database.get_active_events()
        for event in events:
            if event['type'] == 'x2win':
                win_amount *= 2
                break
    
    # Update balance
    if won:
        await database.update_balance(message.from_user.id, win_amount, add=True)
    
    # Add XP
    xp_data = await database.add_xp(message.from_user.id, bet * config.XP_PER_BC)
    
    # Record bet
    await database.record_bet(message.from_user.id, bet, won, win_amount)
    
    if won:
        text = f"✅ <b>Победа!</b>\n\nВыигрыш: <b>+{format_number(win_amount)} BC</b>"
    else:
        text = f"❌ <b>Проигрыш</b>\n\nПотеряно: <b>-{format_number(bet)} BC</b>"
    
    if xp_data.get('leveled_up'):
        text += f"\n🎉 <b>Новый уровень {xp_data['new_level']}!</b>"
    
    await message.answer(text, parse_mode="HTML", reply_markup=back_to_games_kb())
    await state.clear()


async def play_slots_game(message: Message, state: FSMContext, bet: int):
    """Play slots game"""
    won, symbols, win_amount = play_slots(bet)
    
    # Apply event multiplier
    if won:
        events = await database.get_active_events()
        for event in events:
            if event['type'] == 'x2win':
                win_amount *= 2
                break
    
    # Update balance
    if won:
        await database.update_balance(message.from_user.id, win_amount, add=True)
    
    # Add XP
    xp_data = await database.add_xp(message.from_user.id, bet * config.XP_PER_BC)
    
    # Record bet
    await database.record_bet(message.from_user.id, bet, won, win_amount)
    
    symbols_str = " ".join(symbols)
    
    if won:
        text = f"🎰 {symbols_str}\n\n✅ <b>Победа!</b>\n\nВыигрыш: <b>+{format_number(win_amount)} BC</b>"
    else:
        text = f"🎰 {symbols_str}\n\n❌ <b>Проигрыш</b>\n\nПотеряно: <b>-{format_number(bet)} BC</b>"
    
    if xp_data.get('leveled_up'):
        text += f"\n🎉 <b>Новый уровень {xp_data['new_level']}!</b>"
    
    await message.answer(text, parse_mode="HTML", reply_markup=back_to_games_kb())
    await state.clear()


async def play_plinko_game(message: Message, state: FSMContext, bet: int):
    """Play plinko game"""
    win_amount, multiplier = play_plinko(bet)
    
    # Apply event multiplier
    events = await database.get_active_events()
    for event in events:
        if event['type'] == 'x2win':
            win_amount *= 2
            break
    
    # Update balance
    await database.update_balance(message.from_user.id, win_amount, add=True)
    
    # Add XP
    xp_data = await database.add_xp(message.from_user.id, bet * config.XP_PER_BC)
    
    # Record bet
    won = win_amount > bet
    await database.record_bet(message.from_user.id, bet, won, win_amount if won else 0)
    
    text = f"⚪ <b>Plinko</b>\n\nМножитель: <b>x{multiplier}</b>\n\nВыигрыш: <b>+{format_number(win_amount)} BC</b>"
    
    if xp_data.get('leveled_up'):
        text += f"\n🎉 <b>Новый уровень {xp_data['new_level']}!</b>"
    
    await message.answer(text, parse_mode="HTML", reply_markup=back_to_games_kb())
    await state.clear()


async def play_crash_game(message: Message, state: FSMContext, bet: int):
    """Play crash game - ask for cashout point"""
    text = """
🚀 <b>Crash</b>

Введите множитель для вывода (1.5 - 100):
Например: 2.5
"""
    
    await state.update_data(bet=bet)
    await state.set_state(GameStates.waiting_for_crash_cashout)
    await message.answer(text, parse_mode="HTML", reply_markup=back_to_games_kb())


@router.message(GameStates.waiting_for_crash_cashout)
@not_banned
async def crash_cashout(message: Message, state: FSMContext):
    """Process crash cashout"""
    try:
        cashout_at = float(message.text)
        
        if cashout_at < 1.0 or cashout_at > 100:
            await message.answer("❌ Множитель должен быть от 1.0 до 100")
            return
        
        data = await state.get_data()
        bet = data.get('bet', 0)
        
        # Play game
        won, crash_point, win_amount = play_crash(bet, cashout_at)
        
        # Apply event multiplier
        if won:
            events = await database.get_active_events()
            for event in events:
                if event['type'] == 'x2win':
                    win_amount *= 2
                    break
        
        # Update balance
        if won:
            await database.update_balance(message.from_user.id, win_amount, add=True)
        
        # Add XP
        xp_data = await database.add_xp(message.from_user.id, bet * config.XP_PER_BC)
        
        # Record bet
        await database.record_bet(message.from_user.id, bet, won, win_amount)
        
        if won:
            text = f"🚀 <b>Crash</b>\n\nВаш вывод: <b>x{cashout_at}</b>\nКраш: <b>x{crash_point}</b>\n\n✅ Успешно!\n\nВыигрыш: <b>+{format_number(win_amount)} BC</b>"
        else:
            text = f"🚀 <b>Crash</b>\n\nВаш вывод: <b>x{cashout_at}</b>\nКраш: <b>x{crash_point}</b>\n\n❌ Краш!\n\nПотеряно: <b>-{format_number(bet)} BC</b>"
        
        if xp_data.get('leveled_up'):
            text += f"\n🎉 <b>Новый уровень {xp_data['new_level']}!</b>"
        
        await message.answer(text, parse_mode="HTML", reply_markup=back_to_games_kb())
        await state.clear()
        
    except ValueError:
        await message.answer("❌ Введите корректное число")


async def play_blackjack_game(message: Message, state: FSMContext, bet: int):
    """Start blackjack game"""
    # Deal initial cards
    player_cards = [get_card(), get_card()]
    dealer_cards = [get_card(), get_card()]
    
    player_score = calculate_blackjack_score(player_cards)
    dealer_score = calculate_blackjack_score(dealer_cards)
    
    # Check for blackjack
    if player_score == 21:
        win_amount = int(bet * 2.5)
        await database.update_balance(message.from_user.id, win_amount, add=True)
        await database.record_bet(message.from_user.id, bet, True, win_amount)
        xp_data = await database.add_xp(message.from_user.id, bet * config.XP_PER_BC)
        
        text = f"🃏 <b>Блэкджек!</b>\n\nВаши карты: {' '.join(player_cards)} = {player_score}\n\nВыигрыш: <b>+{format_number(win_amount)} BC</b>"
        
        if xp_data.get('leveled_up'):
            text += f"\n🎉 <b>Новый уровень {xp_data['new_level']}!</b>"
        
        await message.answer(text, parse_mode="HTML", reply_markup=back_to_games_kb())
        await state.clear()
        return
    
    # Save game state
    await state.update_data(
        bet=bet,
        player_cards=player_cards,
        dealer_cards=dealer_cards
    )
    await state.set_state(GameStates.blackjack_playing)
    
    text = f"""
🃏 <b>Блэкджек</b>

Ваши карты: {' '.join(player_cards)} = {player_score}
Карта дилера: {dealer_cards[0]}

Взять карту или хватит?
"""
    
    await message.answer(text, parse_mode="HTML", reply_markup=blackjack_kb())


@router.callback_query(F.data == "bj_hit")
async def blackjack_hit(callback: CallbackQuery, state: FSMContext):
    """Hit in blackjack"""
    data = await state.get_data()
    player_cards = data.get('player_cards', [])
    dealer_cards = data.get('dealer_cards', [])
    bet = data.get('bet', 0)
    
    # Add card
    player_cards.append(get_card())
    player_score = calculate_blackjack_score(player_cards)
    
    # Check bust
    if player_score > 21:
        await database.record_bet(callback.from_user.id, bet, False, 0)
        xp_data = await database.add_xp(callback.from_user.id, bet * config.XP_PER_BC)
        
        text = f"🃏 <b>Перебор!</b>\n\nВаши карты: {' '.join(player_cards)} = {player_score}\n\n❌ Проигрыш: <b>-{format_number(bet)} BC</b>"
        
        if xp_data.get('leveled_up'):
            text += f"\n🎉 <b>Новый уровень {xp_data['new_level']}!</b>"
        
        await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_to_games_kb())
        await state.clear()
        await callback.answer()
        return
    
    # Update state
    await state.update_data(player_cards=player_cards)
    
    text = f"""
🃏 <b>Блэкджек</b>

Ваши карты: {' '.join(player_cards)} = {player_score}
Карта дилера: {dealer_cards[0]}

Взять карту или хватит?
"""
    
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=blackjack_kb())
    await callback.answer()


@router.callback_query(F.data == "bj_stand")
async def blackjack_stand(callback: CallbackQuery, state: FSMContext):
    """Stand in blackjack"""
    data = await state.get_data()
    player_cards = data.get('player_cards', [])
    dealer_cards = data.get('dealer_cards', [])
    bet = data.get('bet', 0)
    
    player_score = calculate_blackjack_score(player_cards)
    dealer_score = calculate_blackjack_score(dealer_cards)
    
    # Dealer draws until 17+
    while dealer_score < 17:
        dealer_cards.append(get_card())
        dealer_score = calculate_blackjack_score(dealer_cards)
    
    # Determine winner
    if dealer_score > 21 or player_score > dealer_score:
        # Player wins
        win_amount = bet * 2
        
        # Apply event multiplier
        events = await database.get_active_events()
        for event in events:
            if event['type'] == 'x2win':
                win_amount *= 2
                break
        
        await database.update_balance(callback.from_user.id, win_amount, add=True)
        await database.record_bet(callback.from_user.id, bet, True, win_amount)
        
        text = f"🃏 <b>Победа!</b>\n\nВаши карты: {' '.join(player_cards)} = {player_score}\nКарты дилера: {' '.join(dealer_cards)} = {dealer_score}\n\nВыигрыш: <b>+{format_number(win_amount)} BC</b>"
    elif player_score == dealer_score:
        # Push
        await database.update_balance(callback.from_user.id, bet, add=True)
        text = f"🃏 <b>Ничья!</b>\n\nВаши карты: {' '.join(player_cards)} = {player_score}\nКарты дилера: {' '.join(dealer_cards)} = {dealer_score}\n\nСтавка возвращена"
    else:
        # Dealer wins
        await database.record_bet(callback.from_user.id, bet, False, 0)
        text = f"🃏 <b>Проигрыш</b>\n\nВаши карты: {' '.join(player_cards)} = {player_score}\nКарты дилера: {' '.join(dealer_cards)} = {dealer_score}\n\nПотеряно: <b>-{format_number(bet)} BC</b>"
    
    xp_data = await database.add_xp(callback.from_user.id, bet * config.XP_PER_BC)
    
    if xp_data.get('leveled_up'):
        text += f"\n🎉 <b>Новый уровень {xp_data['new_level']}!</b>"
    
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=back_to_games_kb())
    await state.clear()
    await callback.answer()


# Placeholder for upcoming games
@router.callback_query(F.data.in_(["game_mines", "game_tower", "game_hilo", "game_jackpot", "game_duel"]))
async def game_coming_soon(callback: CallbackQuery):
    """Coming soon games"""
    await callback.answer("🚧 Эта игра скоро будет доступна!", show_alert=True)
