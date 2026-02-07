# 🎰 Black Win Telegram Bot - Project Summary

## Overview

A fully-featured Telegram casino bot built with Python, aiogram 3.x, and Supabase. This bot provides a complete gambling experience with 9 games, economy system, progression mechanics, and comprehensive admin controls.

## Key Statistics

- **Total Lines of Code**: ~2,849
- **Python Files**: 17
- **Games Implemented**: 9 (5 more planned)
- **Database Tables**: 7
- **Commands**: 20+
- **Documentation Pages**: 6
- **Development Status**: Production Ready ✅

## What's Included

### Core Features
✅ 9 Gambling Games (50/50, Roulette, Dice, Crash, Coin, Wheel, Slots, Blackjack, Plinko)  
✅ Virtual Currency Economy (BC - Black Coins)  
✅ Bank System (5% daily interest)  
✅ Level & XP Progression (1-100+)  
✅ Daily Bonuses (500-5,000 BC)  
✅ Promo Code System  
✅ Case Shop (4 tiers)  
✅ Events System (x2 XP, x2 WIN, x2 DAILY)  
✅ Role-based Permissions (Owner, Admin, User)  
✅ Leaderboards  
✅ Admin Panel  
✅ User Statistics  
✅ Ban System  

### Technical Features
✅ Async/Await Architecture  
✅ Supabase Database Integration  
✅ Replit 24/7 Hosting Support  
✅ Keep-Alive Server  
✅ State Management (FSM)  
✅ Inline Keyboards  
✅ Error Handling  
✅ Input Validation  
✅ Access Control  
✅ Comprehensive Logging  

## File Structure

```
BlackWinTG/
├── 📄 Documentation
│   ├── README.md           # Project overview
│   ├── SETUP.md            # Setup instructions
│   ├── DATABASE.md         # Database schema
│   ├── FEATURES.md         # Feature list
│   ├── CHANGELOG.md        # Version history
│   └── TROUBLESHOOTING.md  # Debug guide
│
├── 🔧 Configuration
│   ├── .env.example        # Environment template
│   ├── .gitignore          # Git ignore rules
│   ├── .replit             # Replit config
│   ├── replit.nix          # Nix packages
│   ├── requirements.txt    # Python dependencies
│   ├── config.py           # Bot configuration
│   └── start.sh            # Quick start script
│
├── 🎮 Core Application
│   ├── main.py             # Entry point
│   ├── database.py         # Supabase operations
│   ├── keep_alive.py       # Flask server
│
├── 📡 Handlers (Bot Logic)
│   ├── start.py            # Registration, main menu
│   ├── profile.py          # User profiles
│   ├── economy.py          # Bank, promos, daily
│   ├── games.py            # All games (9)
│   ├── shop.py             # Case shop
│   ├── social.py           # Leaderboard
│   └── admin.py            # Admin panel
│
├── ⌨️ Keyboards
│   └── inline.py           # All inline keyboards
│
└── 🛠️ Utilities
    ├── decorators.py       # Access control
    └── helpers.py          # Helper functions
```

## Quick Start

### Prerequisites
1. Python 3.11+
2. Telegram Bot Token (from @BotFather)
3. Supabase Account
4. Your Telegram ID

### 5-Minute Setup

1. **Clone Repository**
   ```bash
   git clone https://github.com/leqwiss18serv-cloud/BlackWinTG.git
   cd BlackWinTG
   ```

2. **Set Up Database**
   - Create Supabase project
   - Run SQL from DATABASE.md
   - Get URL and API key

3. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

4. **Run Bot**
   ```bash
   chmod +x start.sh
   ./start.sh
   ```

### Deploy to Replit
1. Import from GitHub: `leqwiss18serv-cloud/BlackWinTG`
2. Add Secrets (BOT_TOKEN, SUPABASE_URL, SUPABASE_KEY, OWNER_ID)
3. Click "Run"
4. Set up UptimeRobot for 24/7 operation

## Game Catalog

| Game | Emoji | Win % | Multiplier | Description |
|------|-------|-------|------------|-------------|
| Удача 50/50 | 🎲 | 50% | x2 | Simple coin flip |
| Рулетка | 🎡 | 33% | x3 | Red/Black/Green wheel |
| Кости | 🎯 | 16.7% | x6 | Guess the dice |
| Crash | 🚀 | Variable | up to x100 | Cash out before crash |
| Монетка | 🪙 | 50% | x2 | Heads or tails |
| Колесо | 🎪 | 10% | x10 | High risk, high reward |
| Слоты | 🎰 | Variable | up to x50 | 3 symbol slots |
| Блэкджек | 🃏 | ~48% | x2-x2.5 | Classic 21 |
| Plinko | ⚪ | 100% | x1-x50 | Ball drop game |

## Command Reference

### User Commands
```
/start      - Welcome & registration
/profile    - View your profile
/games      - Browse games
/balance    - Check balance
/bank       - Bank operations
/shop       - Open cases
/daily      - Daily bonus
/promo CODE - Use promo code
/top        - Leaderboards
```

### Admin Commands (Owner Only)
```
/admin                              - Admin panel
/ban USER_ID REASON                 - Ban user
/unban USER_ID                      - Unban user
/addbal USER_ID AMOUNT              - Add balance
/setbal USER_ID AMOUNT              - Set balance
/addadmin USER_ID                   - Make admin
/removeadmin USER_ID                - Remove admin
/createpromo CODE AMOUNT USES       - Create promo
/broadcast MESSAGE                  - Send to all
/stats                              - Bot statistics
```

## Database Tables

1. **users** - User accounts, balances, stats
2. **friends** - Friend relationships
3. **promocodes** - Promo code definitions
4. **promo_uses** - Promo code usage tracking
5. **events** - Active events (x2 XP, etc.)
6. **jackpot** - Jackpot game state
7. **duels** - PvP duel matches

## Dependencies

```
aiogram==3.4.1      # Telegram Bot framework
aiohttp==3.9.3      # Async HTTP client
supabase==2.3.4     # Database client
python-dotenv==1.0.1 # Environment vars
flask==3.0.2        # Keep-alive server
```

## Configuration Variables

Required in `.env` or Replit Secrets:

```bash
BOT_TOKEN=your_bot_token           # From @BotFather
SUPABASE_URL=your_supabase_url     # From Supabase dashboard
SUPABASE_KEY=your_supabase_key     # From Supabase dashboard
OWNER_ID=your_telegram_id          # From @userinfobot
OWNER_USERNAME=kLeqwiss            # Your username
```

## Future Roadmap

### v1.1.0 (Planned)
- 💣 Мины game
- 🏰 Башня game
- 👥 Friends system
- 🏆 Achievements

### v1.2.0 (Planned)
- 💰 Jackpot game
- ⚔️ Дуэли (PvP)
- 🎯 Daily quests
- 🎪 Tournaments

## Support & Documentation

- **Setup Guide**: See SETUP.md
- **Features List**: See FEATURES.md
- **Database Schema**: See DATABASE.md
- **Troubleshooting**: See TROUBLESHOOTING.md
- **Changelog**: See CHANGELOG.md
- **Telegram**: @kLeqwiss
- **GitHub**: https://github.com/leqwiss18serv-cloud/BlackWinTG

## Testing Checklist

Before going live:

- [ ] Database tables created
- [ ] Environment variables set
- [ ] Bot responds to /start
- [ ] Games work correctly
- [ ] Balance updates properly
- [ ] Admin commands work
- [ ] Daily bonus claimable
- [ ] Promo codes activate
- [ ] Shop opens cases
- [ ] Leaderboard displays
- [ ] Events can be created
- [ ] Keep-alive server running

## Security Checklist

- [ ] Bot token kept private
- [ ] Supabase credentials secure
- [ ] Owner ID correctly set
- [ ] .env not committed to git
- [ ] Access control tested
- [ ] Ban system working
- [ ] Input validation active

## Performance Tips

1. **Database**: Ensure all indexes created (see DATABASE.md)
2. **Hosting**: Use UptimeRobot for 24/7 uptime
3. **Monitoring**: Check logs regularly
4. **Backups**: Export Supabase weekly
5. **Updates**: Keep dependencies current

## Common Customizations

### Change Starting Balance
```python
# config.py
INITIAL_BALANCE = 50000  # Changed from 10000
```

### Adjust Bank Interest
```python
# config.py
BANK_INTEREST_RATE = 0.10  # 10% instead of 5%
```

### Modify Game Odds
```python
# utils/helpers.py - Example for 50/50 game
def play_5050(bet: int) -> tuple[bool, int]:
    won = random.random() < 0.6  # 60% instead of 50%
    # ...
```

### Change Bet Limits
```python
# config.py
GAME_MIN_BET = 500      # Higher minimum
GAME_MAX_BET = 10000000 # Higher maximum
```

## Credits

- **Developer**: @kLeqwiss
- **Framework**: aiogram 3.x
- **Database**: Supabase (PostgreSQL)
- **Hosting**: Replit
- **Original**: BlackWin web application

## License

MIT License - Free to use and modify

## Version

**Current Version**: 1.0.0  
**Release Date**: February 7, 2026  
**Status**: Production Ready ✅

---

## Quick Links

- 📚 [Full Documentation](README.md)
- 🚀 [Setup Guide](SETUP.md)
- 💾 [Database Schema](DATABASE.md)
- ✨ [Features List](FEATURES.md)
- 🔧 [Troubleshooting](TROUBLESHOOTING.md)
- 📝 [Changelog](CHANGELOG.md)

---

**Ready to deploy?** Follow the [SETUP.md](SETUP.md) guide!  
**Need help?** Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)!  
**Want to customize?** See source code and modify!

🎰 **Happy Gaming!** 🎰
