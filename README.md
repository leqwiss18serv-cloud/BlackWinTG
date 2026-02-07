# Black Win Telegram Bot 🎰

A comprehensive casino Telegram bot built with Python, aiogram 3.x, and Supabase.

## Features

### 🎮 Games
- **Удача 50/50** 🎲 - 50% chance, x2 win
- **Рулетка X3** 🎡 - Red/Black/Green, x3 win
- **Кости X6** 🎯 - Guess 1-6, x6 win
- **Crash X100** 🚀 - Cash out before crash, up to x100
- **Монетка X2** 🪙 - Heads/Tails, x2 win
- **Колесо X10** 🎪 - 10% chance, x10 win
- **Слоты** 🎰 - 3 symbols, up to x50
- **Блэкджек** 🃏 - Classic 21 game
- **Plinko** ⚪ - Ball drop, multipliers x1-x50

### 💰 Economy System
- Virtual currency: BC (Black Coins)
- Starting balance: 10,000 BC
- Bank with 5% daily interest
- Daily bonuses (500-5,000 BC)
- Promo codes (single/multi-use)
- Case shop (4 tiers)

### 📊 Progression System
- Levels 1-100+
- XP per bet (1 BC = 1 XP)
- Level-based rewards
- Achievements system
- Leaderboards (balance & level)

### 🛡️ Role System
- **Owner** (@kLeqwiss) - Full control
- **Admins** - Event management, moderation
- **Users** - Regular players

### 🎉 Events System
- x2 XP events
- x2 WIN multipliers
- x2 DAILY bonuses
- Timed events with global notifications

## Installation

### Requirements
- Python 3.11+
- Supabase account
- Telegram Bot Token

### Setup

1. Clone the repository:
```bash
git clone https://github.com/leqwiss18serv-cloud/BlackWinTG.git
cd BlackWinTG
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```bash
cp .env.example .env
```

4. Configure environment variables in `.env`:
```
BOT_TOKEN=your_bot_token_here
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_key_here
OWNER_ID=your_telegram_id
OWNER_USERNAME=kLeqwiss
```

5. Set up the database:
   - Go to your Supabase project
   - Run the SQL commands from `DATABASE.md`
   - Create all tables and indexes

6. Run the bot:
```bash
python main.py
```

## Deployment on Replit

1. Import this repository to Replit
2. Set up Secrets (environment variables)
3. Click "Run"
4. The bot will run 24/7 with keep-alive server

## Project Structure

```
BlackWinTG/
├── main.py                 # Entry point
├── config.py               # Configuration
├── database.py             # Supabase operations
├── keep_alive.py           # Flask server for 24/7
├── handlers/
│   ├── start.py            # /start, main menu
│   ├── profile.py          # User profiles
│   ├── economy.py          # Bank, promos, daily
│   ├── games.py            # All games
│   ├── shop.py             # Case shop
│   ├── social.py           # Friends, leaderboard
│   └── admin.py            # Admin panel
├── keyboards/
│   └── inline.py           # All inline keyboards
├── utils/
│   ├── decorators.py       # Access control
│   └── helpers.py          # Helper functions
├── requirements.txt
├── .replit
├── replit.nix
└── DATABASE.md             # Database schema
```

## Commands

### User Commands
- `/start` - Main menu
- `/profile` - View profile
- `/games` - Games list
- `/balance` - Check balance
- `/bank` - Bank operations
- `/shop` - Case shop
- `/friends` - Friends system
- `/top` - Leaderboard
- `/daily` - Daily bonus
- `/promo [code]` - Activate promo

### Admin Commands (Owner only)
- `/admin` - Admin panel
- `/broadcast [text]` - Broadcast message
- `/ban [user_id] [reason]` - Ban user
- `/unban [user_id]` - Unban user
- `/addbal [user_id] [amount]` - Add BC
- `/setbal [user_id] [amount]` - Set BC
- `/addadmin [user_id]` - Add admin
- `/removeadmin [user_id]` - Remove admin
- `/createpromo [code] [amount] [uses]` - Create promo
- `/stats` - Bot statistics

## Game Rules

### Удача 50/50
Simple 50% chance game with x2 multiplier.

### Рулетка X3
Choose Red, Black, or Green. Each color has ~33% chance, x3 win.

### Кости X6
Guess a number 1-6. 16.7% chance, x6 win.

### Crash X100
Set a cashout multiplier (1.0-100x). If the crash point is higher, you win!

### Монетка X2
Heads or Tails. 50% chance, x2 win.

### Колесо X10
10% chance to win, x10 multiplier.

### Слоты
Match 3 symbols:
- 🍒🍒🍒 = x5
- 🍋🍋🍋 = x10
- 🍊🍊🍊 = x15
- 🍇🍇🍇 = x20
- 💎💎💎 = x30
- 7️⃣7️⃣7️⃣ = x50

### Блэкджек
Classic 21 game. Beat the dealer without going over 21.

### Plinko
Ball drops through pegs. Land in slots with multipliers x1-x50.

## Case Shop

| Case | Price | Reward Range |
|------|-------|--------------|
| Обычный | 1,000 BC | 500-2,000 BC |
| Редкий | 5,000 BC | 2,000-15,000 BC |
| Эпический | 25,000 BC | 10,000-100,000 BC |
| Легендарный | 100,000 BC | 50,000-500,000 BC |

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Support

For support, contact @kLeqwiss on Telegram.

## Credits

Developed by @kLeqwiss
Original web version: [BlackWin](https://github.com/leqwiss18serv-cloud/BlackWin)
