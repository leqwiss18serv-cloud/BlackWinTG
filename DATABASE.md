# Black Win Bot - Database Schema

This document describes the database schema for the Black Win Telegram bot using Supabase (PostgreSQL).

## Tables

### users

Main table for storing user data.

```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY,                    -- Telegram user ID
    username TEXT NOT NULL,                   -- Telegram username
    balance BIGINT DEFAULT 10000,             -- Current BC balance
    bank_balance BIGINT DEFAULT 0,            -- BC in bank
    xp BIGINT DEFAULT 0,                      -- Experience points
    level INTEGER DEFAULT 1,                  -- Current level
    is_banned BOOLEAN DEFAULT false,          -- Ban status
    ban_reason TEXT,                          -- Reason for ban
    role TEXT DEFAULT 'user',                 -- user/admin/owner
    total_won BIGINT DEFAULT 0,               -- Total BC won
    total_lost BIGINT DEFAULT 0,              -- Total BC lost
    total_bets INTEGER DEFAULT 0,             -- Number of bets made
    wins INTEGER DEFAULT 0,                   -- Number of wins
    last_daily TIMESTAMP WITH TIME ZONE,      -- Last daily bonus claim
    last_bank_interest TIMESTAMP WITH TIME ZONE, -- Last bank interest calculation
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_balance ON users(balance DESC);
CREATE INDEX idx_users_level ON users(level DESC, xp DESC);
```

### friends

Table for managing friend relationships.

```sql
CREATE TABLE friends (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    friend_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    status TEXT DEFAULT 'pending',            -- pending/accepted
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, friend_id)
);

-- Indexes
CREATE INDEX idx_friends_user ON friends(user_id);
CREATE INDEX idx_friends_status ON friends(status);
```

### promocodes

Table for promo codes.

```sql
CREATE TABLE promocodes (
    id SERIAL PRIMARY KEY,
    code TEXT UNIQUE NOT NULL,                -- Promo code
    amount BIGINT NOT NULL,                   -- BC reward amount
    max_uses INTEGER NOT NULL,                -- Maximum number of uses
    uses INTEGER DEFAULT 0,                   -- Current number of uses
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL, -- Expiration date
    created_by BIGINT REFERENCES users(id),   -- Creator user ID
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_promocodes_code ON promocodes(code);
CREATE INDEX idx_promocodes_expires ON promocodes(expires_at);
```

### promo_uses

Table for tracking promo code usage by users.

```sql
CREATE TABLE promo_uses (
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    promo_id INTEGER REFERENCES promocodes(id) ON DELETE CASCADE,
    used_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (user_id, promo_id)
);

-- Indexes
CREATE INDEX idx_promo_uses_user ON promo_uses(user_id);
CREATE INDEX idx_promo_uses_promo ON promo_uses(promo_id);
```

### events

Table for active events (x2 XP, x2 WIN, etc.).

```sql
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    type TEXT NOT NULL,                       -- x2xp/x2win/x2daily
    ends_at TIMESTAMP WITH TIME ZONE NOT NULL, -- Event end time
    created_by BIGINT REFERENCES users(id),   -- Creator user ID
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_events_ends_at ON events(ends_at);
CREATE INDEX idx_events_type ON events(type);
```

### jackpot

Table for jackpot game state.

```sql
CREATE TABLE jackpot (
    id SERIAL PRIMARY KEY,
    pool BIGINT DEFAULT 0,                    -- Current jackpot pool
    participants JSONB DEFAULT '[]'::jsonb,   -- Array of participant data
    last_draw TIMESTAMP WITH TIME ZONE,       -- Last jackpot draw time
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### duels

Table for PvP duels.

```sql
CREATE TABLE duels (
    id SERIAL PRIMARY KEY,
    creator_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    opponent_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    amount BIGINT NOT NULL,                   -- Bet amount
    status TEXT DEFAULT 'pending',            -- pending/active/finished
    winner_id BIGINT REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    finished_at TIMESTAMP WITH TIME ZONE
);

-- Indexes
CREATE INDEX idx_duels_creator ON duels(creator_id);
CREATE INDEX idx_duels_opponent ON duels(opponent_id);
CREATE INDEX idx_duels_status ON duels(status);
```

## Initial Setup

After creating the tables, set up the owner user:

```sql
-- Update owner role (replace with actual Telegram ID)
UPDATE users SET role = 'owner' WHERE id = YOUR_TELEGRAM_ID;
```

## Row Level Security (RLS)

For security, enable RLS on sensitive tables:

```sql
-- Enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE promocodes ENABLE ROW LEVEL SECURITY;
ALTER TABLE events ENABLE ROW LEVEL SECURITY;

-- Create policies (examples)
CREATE POLICY "Users can view their own data" ON users
    FOR SELECT USING (auth.uid()::bigint = id);

CREATE POLICY "Only service role can modify users" ON users
    FOR ALL USING (auth.role() = 'service_role');
```

## Maintenance

### Clean up expired promo codes

```sql
DELETE FROM promocodes WHERE expires_at < NOW();
```

### Clean up expired events

```sql
DELETE FROM events WHERE ends_at < NOW();
```

### Calculate bank interest (run daily)

```sql
-- This should be done via a scheduled job or bot logic
UPDATE users
SET bank_balance = bank_balance * 1.05,
    last_bank_interest = NOW()
WHERE last_bank_interest IS NULL 
   OR last_bank_interest < NOW() - INTERVAL '24 hours';
```

## Indexes for Performance

The schema includes indexes on:
- User lookups by ID (primary key)
- Role-based queries
- Leaderboard queries (balance, level)
- Friend relationships
- Promo code lookups
- Event expiration checks

## Notes

1. All timestamps use `TIMESTAMP WITH TIME ZONE` for proper timezone handling
2. Foreign keys use `ON DELETE CASCADE` where appropriate
3. Unique constraints prevent duplicate data
4. Default values simplify new user creation
5. JSONB is used for flexible data structures (e.g., jackpot participants)
