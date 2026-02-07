# Setup Guide - Black Win Telegram Bot

## Prerequisites

1. **Telegram Bot Token**
   - Open Telegram and search for @BotFather
   - Send `/newbot` and follow the instructions
   - Save the token provided

2. **Supabase Account**
   - Sign up at https://supabase.com
   - Create a new project
   - Wait for database to be ready

3. **Your Telegram ID**
   - Message @userinfobot on Telegram to get your user ID
   - Save this number as OWNER_ID

## Step 1: Database Setup

1. Go to your Supabase project dashboard
2. Click on "SQL Editor" in the left sidebar
3. Create a new query
4. Copy and paste the following SQL (all tables):

```sql
-- Users table
CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    username TEXT NOT NULL,
    balance BIGINT DEFAULT 10000,
    bank_balance BIGINT DEFAULT 0,
    xp BIGINT DEFAULT 0,
    level INTEGER DEFAULT 1,
    is_banned BOOLEAN DEFAULT false,
    ban_reason TEXT,
    role TEXT DEFAULT 'user',
    total_won BIGINT DEFAULT 0,
    total_lost BIGINT DEFAULT 0,
    total_bets INTEGER DEFAULT 0,
    wins INTEGER DEFAULT 0,
    last_daily TIMESTAMP WITH TIME ZONE,
    last_bank_interest TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_balance ON users(balance DESC);
CREATE INDEX idx_users_level ON users(level DESC, xp DESC);

-- Friends table
CREATE TABLE friends (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    friend_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, friend_id)
);

CREATE INDEX idx_friends_user ON friends(user_id);
CREATE INDEX idx_friends_status ON friends(status);

-- Promocodes table
CREATE TABLE promocodes (
    id SERIAL PRIMARY KEY,
    code TEXT UNIQUE NOT NULL,
    amount BIGINT NOT NULL,
    max_uses INTEGER NOT NULL,
    uses INTEGER DEFAULT 0,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_by BIGINT REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_promocodes_code ON promocodes(code);
CREATE INDEX idx_promocodes_expires ON promocodes(expires_at);

-- Promo uses table
CREATE TABLE promo_uses (
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    promo_id INTEGER REFERENCES promocodes(id) ON DELETE CASCADE,
    used_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (user_id, promo_id)
);

CREATE INDEX idx_promo_uses_user ON promo_uses(user_id);
CREATE INDEX idx_promo_uses_promo ON promo_uses(promo_id);

-- Events table
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    type TEXT NOT NULL,
    ends_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_by BIGINT REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_events_ends_at ON events(ends_at);
CREATE INDEX idx_events_type ON events(type);

-- Jackpot table
CREATE TABLE jackpot (
    id SERIAL PRIMARY KEY,
    pool BIGINT DEFAULT 0,
    participants JSONB DEFAULT '[]'::jsonb,
    last_draw TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Duels table
CREATE TABLE duels (
    id SERIAL PRIMARY KEY,
    creator_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    opponent_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    amount BIGINT NOT NULL,
    status TEXT DEFAULT 'pending',
    winner_id BIGINT REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    finished_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_duels_creator ON duels(creator_id);
CREATE INDEX idx_duels_opponent ON duels(opponent_id);
CREATE INDEX idx_duels_status ON duels(status);
```

5. Click "RUN" to execute the SQL
6. Verify all tables were created in the "Table Editor"

## Step 2: Get Supabase Credentials

1. In your Supabase project, go to "Settings" → "API"
2. Copy the following:
   - **URL**: Your project URL (looks like https://xxx.supabase.co)
   - **anon/public key**: Your API key (starts with eyJ...)

## Step 3: Local Setup (Optional - for testing)

1. Clone the repository:
```bash
git clone https://github.com/leqwiss18serv-cloud/BlackWinTG.git
cd BlackWinTG
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```bash
BOT_TOKEN=your_bot_token_from_botfather
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
OWNER_ID=your_telegram_id
OWNER_USERNAME=kLeqwiss
```

4. Test the bot:
```bash
python main.py
```

## Step 4: Deploy to Replit

1. Go to https://replit.com
2. Click "Create Repl"
3. Choose "Import from GitHub"
4. Enter: `leqwiss18serv-cloud/BlackWinTG`
5. Click "Import from GitHub"

### Configure Secrets in Replit

1. Click on "Secrets" (lock icon) in left sidebar
2. Add the following secrets:
   - Key: `BOT_TOKEN`, Value: your bot token
   - Key: `SUPABASE_URL`, Value: your Supabase URL
   - Key: `SUPABASE_KEY`, Value: your Supabase key
   - Key: `OWNER_ID`, Value: your Telegram ID (number only)
   - Key: `OWNER_USERNAME`, Value: `kLeqwiss`

### Run the Bot

1. Click the "Run" button
2. The bot will start and show "Bot started successfully!"
3. Open Telegram and search for your bot
4. Send `/start` to begin!

## Step 5: Keep Bot Running 24/7

Replit includes a keep-alive server that responds to HTTP requests.

### Option 1: Use UptimeRobot (Free)

1. Go to https://uptimerobot.com and create account
2. Add new monitor:
   - Monitor Type: HTTP(s)
   - Friendly Name: BlackWinBot
   - URL: Your Replit URL (shown when bot runs)
   - Monitoring Interval: 5 minutes
3. Save monitor

### Option 2: Use Replit Always On (Paid)

1. In Replit, go to your Repl
2. Click "Always On" toggle
3. This keeps the Repl running 24/7

## Verification

Test these commands in your bot:

1. `/start` - Should show welcome message
2. `/profile` - Should show your profile
3. `/games` - Should show games menu
4. `/balance` - Should show 10,000 BC starting balance
5. `/admin` - Should show admin panel (owner only)
6. `/stats` - Should show bot statistics

## Common Issues

### "Bot doesn't respond"
- Check BOT_TOKEN is correct
- Verify bot is running in Replit
- Check Replit logs for errors

### "Database error"
- Verify all tables were created
- Check SUPABASE_URL and SUPABASE_KEY
- Ensure Supabase project is active

### "Permission denied"
- Verify OWNER_ID matches your Telegram ID
- Check that your user has role='owner' in database

## Next Steps

1. **Create First Promo Code**
```
/createpromo WELCOME 5000 100
```

2. **Start an Event**
```
Use /admin → Events → x2 XP
Enter duration in minutes
```

3. **Test Games**
- Try each game to ensure they work
- Check balance updates correctly
- Verify XP and level progression

4. **Customize**
- Edit `config.py` for game settings
- Modify messages in handlers
- Adjust multipliers and odds

## Security Tips

1. Never share your `.env` file or Replit secrets
2. Keep your bot token private
3. Regularly check admin list
4. Monitor bot statistics for unusual activity
5. Back up your Supabase database regularly

## Support

If you encounter issues:
1. Check the logs in Replit console
2. Review DATABASE.md for schema details
3. Contact @kLeqwiss on Telegram

## Maintenance

### Weekly
- Review active promocodes
- Check event schedule
- Monitor top players

### Monthly
- Database cleanup (expired promos/events)
- Backup database
- Review bot statistics
- Update dependencies if needed

Enjoy your Black Win Casino Bot! 🎰
