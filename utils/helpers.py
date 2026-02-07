import random
from datetime import datetime, timedelta
from typing import Dict, List


def format_number(num: int) -> str:
    """Format number with thousand separators"""
    return f"{num:,}".replace(',', ' ')


def format_balance(balance: int) -> str:
    """Format balance with BC suffix"""
    return f"{format_number(balance)} BC"


def calculate_level_xp(level: int) -> int:
    """Calculate total XP needed to reach level"""
    total = 0
    for i in range(1, level):
        total += 1000 + (i - 1) * 100
    return total


def get_xp_for_next_level(current_level: int) -> int:
    """Get XP needed for next level"""
    return 1000 + (current_level - 1) * 100


def get_progress_bar(current: int, total: int, length: int = 10) -> str:
    """Create a progress bar"""
    filled = int((current / total) * length)
    bar = '█' * filled + '░' * (length - filled)
    percentage = int((current / total) * 100)
    return f"[{bar}] {percentage}%"


def get_random_daily_bonus() -> int:
    """Get random daily bonus amount"""
    return random.randint(500, 5000)


def format_time_remaining(end_time: datetime) -> str:
    """Format time remaining until datetime"""
    now = datetime.utcnow()
    if isinstance(end_time, str):
        end_time = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
    
    delta = end_time - now
    if delta.total_seconds() <= 0:
        return "Истёк"
    
    hours = int(delta.total_seconds() // 3600)
    minutes = int((delta.total_seconds() % 3600) // 60)
    seconds = int(delta.total_seconds() % 60)
    
    if hours > 0:
        return f"{hours}ч {minutes}м"
    elif minutes > 0:
        return f"{minutes}м {seconds}с"
    else:
        return f"{seconds}с"


def get_rank_emoji(rank: int) -> str:
    """Get emoji for leaderboard rank"""
    if rank == 1:
        return "🥇"
    elif rank == 2:
        return "🥈"
    elif rank == 3:
        return "🥉"
    else:
        return f"{rank}."


# Game logic helpers
def play_dice_game(bet: int, choice: int) -> tuple[bool, int, int]:
    """
    Play dice game (1-6)
    Returns: (won, rolled_number, win_amount)
    """
    roll = random.randint(1, 6)
    won = roll == choice
    win_amount = bet * 6 if won else 0
    return won, roll, win_amount


def play_coin_flip(bet: int, choice: str) -> tuple[bool, str, int]:
    """
    Play coin flip
    Returns: (won, result, win_amount)
    """
    result = random.choice(['heads', 'tails'])
    won = result == choice
    win_amount = bet * 2 if won else 0
    return won, result, win_amount


def play_5050(bet: int) -> tuple[bool, int]:
    """
    Play 50/50 game
    Returns: (won, win_amount)
    """
    won = random.random() < 0.5
    win_amount = bet * 2 if won else 0
    return won, win_amount


def play_roulette(bet: int, choice: str) -> tuple[bool, str, int]:
    """
    Play roulette (red/black/green)
    Returns: (won, result, win_amount)
    """
    result = random.choices(['red', 'black', 'green'], weights=[0.45, 0.45, 0.10])[0]
    won = result == choice
    win_amount = bet * 3 if won else 0
    return won, result, win_amount


def play_wheel(bet: int) -> tuple[bool, int]:
    """
    Play wheel x10
    Returns: (won, win_amount)
    """
    won = random.random() < 0.1
    win_amount = bet * 10 if won else 0
    return won, win_amount


def play_slots(bet: int) -> tuple[bool, List[str], int]:
    """
    Play slots
    Returns: (won, symbols, win_amount)
    """
    symbols = ['🍒', '🍋', '🍊', '🍇', '💎', '7️⃣']
    weights = [30, 25, 20, 15, 8, 2]
    
    result = random.choices(symbols, weights=weights, k=3)
    
    # Check win
    if result[0] == result[1] == result[2]:
        # All match
        multipliers = {'🍒': 5, '🍋': 10, '🍊': 15, '🍇': 20, '💎': 30, '7️⃣': 50}
        multiplier = multipliers.get(result[0], 5)
        win_amount = bet * multiplier
        won = True
    elif result[0] == result[1] or result[1] == result[2]:
        # Two match
        win_amount = bet * 2
        won = True
    else:
        won = False
        win_amount = 0
    
    return won, result, win_amount


def play_crash(bet: int, cashout_at: float) -> tuple[bool, float, int]:
    """
    Play crash game
    Returns: (won, crash_point, win_amount)
    """
    # Generate crash point (exponential distribution)
    crash_point = 1.0
    while random.random() > 0.01:  # 1% chance to crash each step
        crash_point += 0.01
        if crash_point >= 100:
            break
    
    crash_point = round(crash_point, 2)
    
    if cashout_at <= crash_point:
        win_amount = int(bet * cashout_at)
        won = True
    else:
        win_amount = 0
        won = False
    
    return won, crash_point, win_amount


def play_plinko(bet: int) -> tuple[int, float]:
    """
    Play plinko
    Returns: (win_amount, multiplier)
    """
    # Simulate ball dropping through pegs
    position = 8  # Start in middle
    
    for _ in range(12):  # 12 rows
        position += random.choice([-1, 1])
        position = max(0, min(16, position))
    
    # Multipliers based on final position (bell curve)
    multipliers = [50, 25, 10, 5, 3, 2, 1.5, 1, 1, 1.5, 2, 3, 5, 10, 25, 50]
    multiplier = multipliers[position] if position < len(multipliers) else 1
    
    win_amount = int(bet * multiplier)
    return win_amount, multiplier


def calculate_blackjack_score(cards: List[str]) -> int:
    """Calculate blackjack hand score"""
    score = 0
    aces = 0
    
    for card in cards:
        if card in ['J', 'Q', 'K']:
            score += 10
        elif card == 'A':
            aces += 1
            score += 11
        else:
            score += int(card)
    
    # Adjust for aces
    while score > 21 and aces > 0:
        score -= 10
        aces -= 1
    
    return score


def get_card() -> str:
    """Get random card"""
    cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    return random.choice(cards)
