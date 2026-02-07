# Black Win Bot - Complete Features List

## 🎮 Games (14 Total)

### Implemented Games (9)

#### 1. Удача 50/50 🎲
- **Win Chance**: 50%
- **Multiplier**: x2
- **How to Play**: Simply place a bet, instant result
- **Min Bet**: 100 BC
- **Max Bet**: 1,000,000 BC

#### 2. Рулетка X3 🎡
- **Win Chance**: 33% (each color)
- **Multiplier**: x3
- **Colors**: Red 🔴, Black ⚫, Green 🟢
- **How to Play**: Choose a color, spin the wheel

#### 3. Кости X6 🎯
- **Win Chance**: 16.7% (1/6)
- **Multiplier**: x6
- **Numbers**: 1, 2, 3, 4, 5, 6
- **How to Play**: Guess the dice roll

#### 4. Crash X100 🚀
- **Win Chance**: Variable
- **Multiplier**: 1.0x - 100x
- **How to Play**: Set cashout multiplier, pray it doesn't crash before
- **Strategy**: Higher cashout = higher risk

#### 5. Монетка X2 🪙
- **Win Chance**: 50%
- **Multiplier**: x2
- **Sides**: Heads 🦅, Tails 🌟
- **How to Play**: Pick a side, flip the coin

#### 6. Колесо X10 🎪
- **Win Chance**: 10%
- **Multiplier**: x10
- **How to Play**: Spin the wheel, high risk high reward

#### 7. Слоты 🎰
- **Win Chance**: Variable
- **Multipliers**: x2 - x50
- **Symbols**: 
  - 🍒 Cherry (x5)
  - 🍋 Lemon (x10)
  - 🍊 Orange (x15)
  - 🍇 Grape (x20)
  - 💎 Diamond (x30)
  - 7️⃣ Seven (x50)
- **How to Play**: Spin 3 reels, match symbols

#### 8. Блэкджек 🃏
- **Win Chance**: Skill-based (~48%)
- **Multiplier**: x2 (x2.5 for blackjack)
- **How to Play**: Classic 21 game
- **Actions**: Hit (take card), Stand (hold)
- **Goal**: Beat dealer without going over 21

#### 9. Plinko ⚪
- **Win Chance**: 100% (always win something)
- **Multipliers**: x1 - x50 (bell curve)
- **How to Play**: Ball drops through pegs
- **Pattern**: Center = lower multipliers, edges = higher

### Coming Soon (5)

#### 10. Мины 5x5 💣
- Grid-based minesweeper
- Progressive multipliers
- Cash out anytime
- Risk vs reward gameplay

#### 11. Башня 🏰
- 10 floors to climb
- Choose correct path each floor
- Multiplier increases per floor
- Cash out or risk it all

#### 12. Выше/Ниже 📊
- Guess if next number is higher or lower
- Chain wins for bigger multipliers
- 50/50 each round

#### 13. Джекпот 💰
- Community pot
- Everyone contributes
- Random draw every 5 minutes
- Winner takes all (minus house edge)

#### 14. Дуэли ⚔️
- PvP betting
- Challenge other players
- 50/50 chance
- Winner takes pot

## 💰 Economy System

### Virtual Currency
- **Name**: BC (Black Coins)
- **Starting Balance**: 10,000 BC
- **Earn Methods**:
  - Win games
  - Daily bonuses
  - Promo codes
  - Case shop
  - Bank interest

### Bank System
- **Interest Rate**: 5% daily
- **Compounding**: Daily
- **Operations**:
  - Deposit (from wallet to bank)
  - Withdraw (from bank to wallet)
- **Safety**: Funds in bank safe from losses
- **Strategy**: Store winnings for passive income

### Daily Bonus
- **Frequency**: Once per 24 hours
- **Amount**: Random 500-5,000 BC
- **Multiplier**: Can be 2x during events
- **Command**: `/daily`

### Promo Codes
- **Types**:
  - Single-use (one user only)
  - Multi-use (limited uses)
  - Limited time (expires after X days)
- **Rewards**: BC amount set by admin
- **Creation**: Owner only (`/createpromo`)
- **Activation**: `/promo CODE`

## 📊 Progression System

### Levels & XP
- **Starting Level**: 1
- **Max Level**: No limit (100+)
- **XP Gain**: 1 XP per 1 BC bet
- **Level Calculation**: 
  - Level 1→2: 1,000 XP
  - Level 2→3: 1,100 XP
  - Level 3→4: 1,200 XP
  - Increases by 100 XP each level
- **Benefits**: 
  - Status symbol
  - Leaderboard ranking
  - Future: Level-based rewards

### Statistics Tracking
- **Total Bets**: Number of games played
- **Total Wins**: Number of games won
- **Win Rate**: Percentage of wins
- **Total Won**: BC won from games
- **Total Lost**: BC lost to games
- **Net Profit**: Total won - Total lost

### Leaderboards
- **Top 10 by Balance**: Richest players
- **Top 10 by Level**: Highest level players
- **Real-time Updates**: Auto-updates
- **Medals**: 🥇 🥈 🥉 for top 3

## 🛍️ Shop System

### Case Shop
| Case | Price | Min Reward | Max Reward | Expected Return |
|------|-------|------------|------------|----------------|
| 📦 Обычный | 1,000 BC | 500 BC | 2,000 BC | ~75% |
| 📦 Редкий | 5,000 BC | 2,000 BC | 15,000 BC | ~85% |
| 📦 Эпический | 25,000 BC | 10,000 BC | 100,000 BC | ~110% |
| 📦 Легендарный | 100,000 BC | 50,000 BC | 500,000 BC | ~137.5% |

- **How It Works**: Pay price, get random reward
- **Strategy**: Higher tier = better odds
- **RNG**: Truly random distribution

## 🎉 Events System

### Event Types

#### 1. x2 XP ✨
- Double XP on all bets
- Great for leveling up
- Command: `/admin` → Events → x2 XP

#### 2. x2 WIN 💰
- Double all game winnings
- Does not affect bet amount
- Most popular event

#### 3. x2 DAILY 🎁
- Double daily bonus rewards
- 1,000-10,000 BC instead of 500-5,000
- Great for inactive players

### Event Management
- **Duration**: 1-1440 minutes (up to 24 hours)
- **Creation**: Admin/Owner only
- **Notifications**: Global broadcast to all users
- **Multiple**: Can stack different event types
- **Status**: Visible in admin panel

## 🛡️ Role System

### Owner (@kLeqwiss)
**Full Access - All Commands**
- User management (ban/unban)
- Balance manipulation (add/set)
- Admin management (add/remove)
- Promo code creation
- Event management
- Broadcasting
- Statistics viewing
- Everything admins can do

**Commands:**
```
/admin - Admin panel
/ban [user_id] [reason]
/unban [user_id]
/addbal [user_id] [amount]
/setbal [user_id] [amount]
/addadmin [user_id]
/removeadmin [user_id]
/createpromo [code] [amount] [uses]
/broadcast [text]
/stats
```

### Admins 🛡️
**Limited Admin Access**
- Event management
- Statistics viewing
- User monitoring
- Cannot modify balances
- Cannot ban users
- Cannot manage other admins

**Commands:**
```
/admin - Admin panel (limited)
```

### Users 👤
**Standard Access**
- Play all games
- Use economy features
- View profiles & stats
- Use shop
- Social features
- No moderation powers

## 👥 Social Features

### Friends System
- **Status**: Coming Soon 🚧
- **Planned Features**:
  - Send friend requests
  - Accept/decline requests
  - View friends list
  - See online status
  - Send BC gifts
  - Private messaging

### Leaderboards
- **Current**: ✅ Implemented
- **Types**:
  - Balance leaderboard
  - Level leaderboard
- **Display**: Top 10 users
- **Update**: Real-time
- **Access**: `/top` command

## 🔒 Security Features

### User Protection
- **Ban System**: Owner can ban users
- **Reason Tracking**: Ban reasons stored
- **Appeal Process**: Contact owner
- **Decorator**: `@not_banned` prevents banned users from playing

### Rate Limiting
- Built into aiogram
- Prevents spam
- Protects bot from abuse

### Input Validation
- Bet amount checks (min/max)
- Balance verification before bets
- User existence checks
- Role permission checks

### Atomic Transactions
- Balance updates are atomic
- No race conditions
- Consistent state
- Error recovery

## 📱 User Interface

### Inline Keyboards
- **Main Menu**: Quick access to all features
- **Games Menu**: All games listed
- **Admin Panel**: Admin functions
- **Bank Interface**: Deposit/withdraw
- **Shop**: Case selection
- **Dynamic**: Context-aware buttons

### Message Formatting
- **HTML Parsing**: Bold, italic text
- **Emojis**: Visual appeal
- **Number Formatting**: Thousand separators
- **Progress Bars**: Level progress visualization
- **Tables**: Organized data display

## 🔄 Keep-Alive System

### Flask Server
- **Port**: 8080
- **Endpoints**:
  - `/` - Status check
  - `/health` - Health check
- **Purpose**: Keep Replit alive 24/7
- **Integration**: Runs in separate thread

### UptimeRobot Integration
- Ping server every 5 minutes
- Free tier available
- Keeps bot running continuously
- No code changes needed

## 📊 Statistics & Analytics

### Bot Statistics
- Total users count
- Total bets placed
- Total BC won
- Total BC lost
- Available via `/stats` (owner)

### User Statistics
- Per-user tracking
- Win/loss ratio
- Total profit
- Games played
- Visible in `/profile`

## 🔧 Configuration

### Game Settings (config.py)
```python
INITIAL_BALANCE = 10000
BANK_INTEREST_RATE = 0.05  # 5%
DAILY_BONUS_MIN = 500
DAILY_BONUS_MAX = 5000
GAME_MIN_BET = 100
GAME_MAX_BET = 1000000
XP_PER_BC = 1
XP_PER_LEVEL = 1000
```

### Easy Customization
- Edit `config.py` for settings
- Modify multipliers in helpers.py
- Change messages in handlers
- Adjust probabilities in game logic

## 🚀 Performance

### Optimizations
- Async/await architecture
- Database indexing
- Efficient queries
- Minimal API calls
- Caching where appropriate

### Scalability
- Handles thousands of users
- Supabase auto-scaling
- Aiogram built for scale
- No polling bottlenecks

## 📝 Logging

### Log Levels
- INFO: Bot start, commands
- ERROR: Database errors, failures
- DEBUG: Detailed game logic (optional)

### Error Handling
- Try/except blocks throughout
- User-friendly error messages
- Admin notifications for critical errors
- Graceful degradation

## 🔮 Future Features

### Planned
1. Мины game
2. Башня game
3. Выше/Ниже game
4. Джекпот system
5. Дуэли (PvP)
6. Friends system
7. Achievements
8. Daily quests
9. VIP system
10. Seasonal events

### Under Consideration
- Multi-language support
- Voice notifications
- Tournament system
- Referral bonuses
- Mobile app integration
- NFT integration
- Cryptocurrency payments

## 📄 License

MIT License - Free to use and modify

## 🤝 Support

- Telegram: @kLeqwiss
- Issues: GitHub Issues
- Documentation: README.md, SETUP.md, DATABASE.md
