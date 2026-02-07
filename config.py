import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Owner Configuration
OWNER_ID = int(os.getenv("OWNER_ID", 0))
OWNER_USERNAME = os.getenv("OWNER_USERNAME", "kLeqwiss")

# Economy Configuration
INITIAL_BALANCE = 10000
BANK_INTEREST_RATE = 0.05  # 5% daily
DAILY_BONUS_MIN = 500
DAILY_BONUS_MAX = 5000

# Game Configuration
GAME_MIN_BET = 100
GAME_MAX_BET = 1000000

# XP Configuration
XP_PER_BC = 1  # 1 BC bet = 1 XP
XP_PER_LEVEL = 1000  # Base XP needed for level 2, increases by 100 per level
