from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_kb() -> InlineKeyboardMarkup:
    """Main menu keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Игры", callback_data="games")],
        [InlineKeyboardButton(text="👤 Профиль", callback_data="profile"),
         InlineKeyboardButton(text="💰 Баланс", callback_data="balance")],
        [InlineKeyboardButton(text="🏦 Банк", callback_data="bank"),
         InlineKeyboardButton(text="🎁 Бонус", callback_data="daily")],
        [InlineKeyboardButton(text="🛍️ Магазин", callback_data="shop"),
         InlineKeyboardButton(text="👥 Друзья", callback_data="friends")],
        [InlineKeyboardButton(text="🏆 Лидерборд", callback_data="leaderboard")],
    ])


def games_menu_kb() -> InlineKeyboardMarkup:
    """Games menu keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Удача 50/50", callback_data="game_5050")],
        [InlineKeyboardButton(text="🎡 Рулетка X3", callback_data="game_roulette")],
        [InlineKeyboardButton(text="🎯 Кости X6", callback_data="game_dice")],
        [InlineKeyboardButton(text="🚀 Crash X100", callback_data="game_crash")],
        [InlineKeyboardButton(text="🪙 Монетка X2", callback_data="game_coin")],
        [InlineKeyboardButton(text="🎪 Колесо X10", callback_data="game_wheel")],
        [InlineKeyboardButton(text="🎰 Слоты", callback_data="game_slots")],
        [InlineKeyboardButton(text="🃏 Блэкджек", callback_data="game_blackjack")],
        [InlineKeyboardButton(text="💣 Мины 5x5", callback_data="game_mines")],
        [InlineKeyboardButton(text="🏰 Башня", callback_data="game_tower")],
        [InlineKeyboardButton(text="⚪ Plinko", callback_data="game_plinko")],
        [InlineKeyboardButton(text="📊 Выше/Ниже", callback_data="game_hilo")],
        [InlineKeyboardButton(text="💰 Джекпот", callback_data="game_jackpot")],
        [InlineKeyboardButton(text="⚔️ Дуэли", callback_data="game_duel")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ])


def back_to_games_kb() -> InlineKeyboardMarkup:
    """Back to games keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад к играм", callback_data="games")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ])


def back_to_main_kb() -> InlineKeyboardMarkup:
    """Back to main menu keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ])


def coin_flip_kb() -> InlineKeyboardMarkup:
    """Coin flip choice keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🦅 Орёл", callback_data="coin_heads"),
         InlineKeyboardButton(text="🌟 Решка", callback_data="coin_tails")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="games")],
    ])


def roulette_kb() -> InlineKeyboardMarkup:
    """Roulette choice keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔴 Красное", callback_data="roulette_red")],
        [InlineKeyboardButton(text="⚫ Чёрное", callback_data="roulette_black")],
        [InlineKeyboardButton(text="🟢 Зелёное", callback_data="roulette_green")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="games")],
    ])


def dice_kb() -> InlineKeyboardMarkup:
    """Dice choice keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1️⃣", callback_data="dice_1"),
         InlineKeyboardButton(text="2️⃣", callback_data="dice_2"),
         InlineKeyboardButton(text="3️⃣", callback_data="dice_3")],
        [InlineKeyboardButton(text="4️⃣", callback_data="dice_4"),
         InlineKeyboardButton(text="5️⃣", callback_data="dice_5"),
         InlineKeyboardButton(text="6️⃣", callback_data="dice_6")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="games")],
    ])


def bank_kb() -> InlineKeyboardMarkup:
    """Bank operations keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💵 Внести", callback_data="bank_deposit")],
        [InlineKeyboardButton(text="💸 Снять", callback_data="bank_withdraw")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ])


def shop_kb() -> InlineKeyboardMarkup:
    """Shop keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 Обычный кейс (1,000 BC)", callback_data="case_common")],
        [InlineKeyboardButton(text="📦 Редкий кейс (5,000 BC)", callback_data="case_rare")],
        [InlineKeyboardButton(text="📦 Эпический кейс (25,000 BC)", callback_data="case_epic")],
        [InlineKeyboardButton(text="📦 Легендарный кейс (100,000 BC)", callback_data="case_legendary")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ])


def admin_kb() -> InlineKeyboardMarkup:
    """Admin panel keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton(text="📢 Рассылка", callback_data="admin_broadcast")],
        [InlineKeyboardButton(text="🎉 Ивенты", callback_data="admin_events")],
        [InlineKeyboardButton(text="👥 Пользователи", callback_data="admin_users")],
        [InlineKeyboardButton(text="🎟️ Промокоды", callback_data="admin_promos")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ])


def events_kb() -> InlineKeyboardMarkup:
    """Events keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✨ x2 XP", callback_data="event_x2xp")],
        [InlineKeyboardButton(text="💰 x2 WIN", callback_data="event_x2win")],
        [InlineKeyboardButton(text="🎁 x2 DAILY", callback_data="event_x2daily")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="admin")],
    ])


def blackjack_kb() -> InlineKeyboardMarkup:
    """Blackjack action keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👋 Взять карту", callback_data="bj_hit"),
         InlineKeyboardButton(text="✋ Хватит", callback_data="bj_stand")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="games")],
    ])


def confirm_kb(action: str) -> InlineKeyboardMarkup:
    """Confirmation keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Да", callback_data=f"confirm_{action}"),
         InlineKeyboardButton(text="❌ Нет", callback_data=f"cancel_{action}")],
    ])
