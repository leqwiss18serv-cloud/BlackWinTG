from supabase import create_client, Client
from datetime import datetime, timedelta
from typing import Optional, List, Dict
import logging
import config

logger = logging.getLogger(__name__)

# Initialize Supabase client
supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)


# User operations
async def get_user(user_id: int) -> Optional[Dict]:
    """Get user by Telegram ID"""
    try:
        response = supabase.table('users').select('*').eq('id', user_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        logger.error(f"Error getting user {user_id}: {e}")
        return None


async def create_user(user_id: int, username: str) -> Dict:
    """Create new user"""
    try:
        user_data = {
            'id': user_id,
            'username': username,
            'balance': config.INITIAL_BALANCE,
            'bank_balance': 0,
            'xp': 0,
            'level': 1,
            'is_banned': False,
            'role': 'owner' if user_id == config.OWNER_ID else 'user',
            'total_won': 0,
            'total_lost': 0,
            'total_bets': 0,
            'wins': 0,
            'created_at': datetime.utcnow().isoformat()
        }
        response = supabase.table('users').insert(user_data).execute()
        return response.data[0]
    except Exception as e:
        logger.error(f"Error creating user {user_id}: {e}")
        raise


async def update_balance(user_id: int, amount: int, add: bool = True) -> bool:
    """Update user balance (add or set)"""
    try:
        if add:
            user = await get_user(user_id)
            if not user:
                return False
            new_balance = user['balance'] + amount
        else:
            new_balance = amount
        
        supabase.table('users').update({'balance': new_balance}).eq('id', user_id).execute()
        return True
    except Exception as e:
        logger.error(f"Error updating balance for user {user_id}: {e}")
        return False


async def update_bank_balance(user_id: int, amount: int, add: bool = True) -> bool:
    """Update user bank balance"""
    try:
        if add:
            user = await get_user(user_id)
            if not user:
                return False
            new_balance = user['bank_balance'] + amount
        else:
            new_balance = amount
        
        supabase.table('users').update({'bank_balance': new_balance}).eq('id', user_id).execute()
        return True
    except Exception as e:
        logger.error(f"Error updating bank balance for user {user_id}: {e}")
        return False


async def deposit_to_bank(user_id: int, amount: int) -> bool:
    """Deposit BC to bank"""
    try:
        user = await get_user(user_id)
        if not user or user['balance'] < amount:
            return False
        
        # Deduct from balance
        await update_balance(user_id, -amount, add=True)
        # Add to bank
        await update_bank_balance(user_id, amount, add=True)
        return True
    except Exception as e:
        logger.error(f"Error depositing to bank for user {user_id}: {e}")
        return False


async def withdraw_from_bank(user_id: int, amount: int) -> bool:
    """Withdraw BC from bank"""
    try:
        user = await get_user(user_id)
        if not user or user['bank_balance'] < amount:
            return False
        
        # Deduct from bank
        await update_bank_balance(user_id, -amount, add=True)
        # Add to balance
        await update_balance(user_id, amount, add=True)
        return True
    except Exception as e:
        logger.error(f"Error withdrawing from bank for user {user_id}: {e}")
        return False


async def add_xp(user_id: int, xp: int) -> Dict:
    """Add XP and level up if needed"""
    try:
        user = await get_user(user_id)
        if not user:
            return {}
        
        new_xp = user['xp'] + xp
        current_level = user['level']
        
        # Calculate level
        total_xp_needed = 0
        level = 1
        while total_xp_needed <= new_xp:
            level += 1
            total_xp_needed += config.XP_PER_LEVEL + (level - 2) * 100
        
        level -= 1
        
        # Update user
        supabase.table('users').update({
            'xp': new_xp,
            'level': level
        }).eq('id', user_id).execute()
        
        return {
            'leveled_up': level > current_level,
            'new_level': level,
            'xp': new_xp
        }
    except Exception as e:
        logger.error(f"Error adding XP for user {user_id}: {e}")
        return {}


async def record_bet(user_id: int, amount: int, won: bool, win_amount: int = 0):
    """Record bet statistics"""
    try:
        user = await get_user(user_id)
        if not user:
            return
        
        update_data = {
            'total_bets': user['total_bets'] + 1
        }
        
        if won:
            update_data['wins'] = user['wins'] + 1
            update_data['total_won'] = user['total_won'] + win_amount
        else:
            update_data['total_lost'] = user['total_lost'] + amount
        
        supabase.table('users').update(update_data).eq('id', user_id).execute()
    except Exception as e:
        logger.error(f"Error recording bet for user {user_id}: {e}")


async def update_daily_bonus(user_id: int) -> bool:
    """Update last daily bonus timestamp"""
    try:
        supabase.table('users').update({
            'last_daily': datetime.utcnow().isoformat()
        }).eq('id', user_id).execute()
        return True
    except Exception as e:
        logger.error(f"Error updating daily bonus for user {user_id}: {e}")
        return False


async def can_claim_daily(user_id: int) -> bool:
    """Check if user can claim daily bonus"""
    try:
        user = await get_user(user_id)
        if not user or not user.get('last_daily'):
            return True
        
        last_daily = datetime.fromisoformat(user['last_daily'].replace('Z', '+00:00'))
        now = datetime.utcnow()
        return (now - last_daily).total_seconds() >= 86400  # 24 hours
    except Exception as e:
        logger.error(f"Error checking daily for user {user_id}: {e}")
        return False


# Promo codes
async def create_promo(code: str, amount: int, max_uses: int, created_by: int, expires_in_days: int = 30) -> bool:
    """Create a promo code"""
    try:
        promo_data = {
            'code': code,
            'amount': amount,
            'max_uses': max_uses,
            'uses': 0,
            'expires_at': (datetime.utcnow() + timedelta(days=expires_in_days)).isoformat(),
            'created_by': created_by
        }
        supabase.table('promocodes').insert(promo_data).execute()
        return True
    except Exception as e:
        logger.error(f"Error creating promo {code}: {e}")
        return False


async def use_promo(user_id: int, code: str) -> tuple[bool, str]:
    """Use a promo code"""
    try:
        # Get promo
        response = supabase.table('promocodes').select('*').eq('code', code).execute()
        if not response.data:
            return False, "Промокод не найден"
        
        promo = response.data[0]
        
        # Check expiration
        expires_at = datetime.fromisoformat(promo['expires_at'].replace('Z', '+00:00'))
        if datetime.utcnow() > expires_at:
            return False, "Промокод истёк"
        
        # Check uses
        if promo['uses'] >= promo['max_uses']:
            return False, "Промокод исчерпан"
        
        # Check if user already used
        check = supabase.table('promo_uses').select('*').eq('user_id', user_id).eq('promo_id', promo['id']).execute()
        if check.data:
            return False, "Вы уже использовали этот промокод"
        
        # Add promo use
        supabase.table('promo_uses').insert({
            'user_id': user_id,
            'promo_id': promo['id']
        }).execute()
        
        # Update uses
        supabase.table('promocodes').update({
            'uses': promo['uses'] + 1
        }).eq('id', promo['id']).execute()
        
        # Add balance
        await update_balance(user_id, promo['amount'], add=True)
        
        return True, f"Промокод активирован! +{promo['amount']:,} BC"
    except Exception as e:
        logger.error(f"Error using promo {code} for user {user_id}: {e}")
        return False, "Ошибка активации промокода"


# Events
async def create_event(event_type: str, duration_minutes: int, created_by: int) -> bool:
    """Create an event"""
    try:
        event_data = {
            'type': event_type,
            'ends_at': (datetime.utcnow() + timedelta(minutes=duration_minutes)).isoformat(),
            'created_by': created_by
        }
        supabase.table('events').insert(event_data).execute()
        return True
    except Exception as e:
        logger.error(f"Error creating event {event_type}: {e}")
        return False


async def get_active_events() -> List[Dict]:
    """Get active events"""
    try:
        now = datetime.utcnow().isoformat()
        response = supabase.table('events').select('*').gt('ends_at', now).execute()
        return response.data
    except Exception as e:
        logger.error(f"Error getting active events: {e}")
        return []


# Admin operations
async def ban_user(user_id: int, reason: str) -> bool:
    """Ban a user"""
    try:
        supabase.table('users').update({
            'is_banned': True,
            'ban_reason': reason
        }).eq('id', user_id).execute()
        return True
    except Exception as e:
        logger.error(f"Error banning user {user_id}: {e}")
        return False


async def unban_user(user_id: int) -> bool:
    """Unban a user"""
    try:
        supabase.table('users').update({
            'is_banned': False,
            'ban_reason': None
        }).eq('id', user_id).execute()
        return True
    except Exception as e:
        logger.error(f"Error unbanning user {user_id}: {e}")
        return False


async def set_role(user_id: int, role: str) -> bool:
    """Set user role (user/admin/owner)"""
    try:
        supabase.table('users').update({'role': role}).eq('id', user_id).execute()
        return True
    except Exception as e:
        logger.error(f"Error setting role for user {user_id}: {e}")
        return False


# Leaderboard
async def get_top_balance(limit: int = 10) -> List[Dict]:
    """Get top users by balance"""
    try:
        response = supabase.table('users').select('id, username, balance').order('balance', desc=True).limit(limit).execute()
        return response.data
    except Exception as e:
        logger.error(f"Error getting top balance: {e}")
        return []


async def get_top_level(limit: int = 10) -> List[Dict]:
    """Get top users by level"""
    try:
        response = supabase.table('users').select('id, username, level, xp').order('level', desc=True).order('xp', desc=True).limit(limit).execute()
        return response.data
    except Exception as e:
        logger.error(f"Error getting top level: {e}")
        return []


# Statistics
async def get_bot_stats() -> Dict:
    """Get bot statistics"""
    try:
        # Total users
        users_response = supabase.table('users').select('id', count='exact').execute()
        total_users = users_response.count
        
        # Total bets
        stats_response = supabase.table('users').select('total_bets, total_won, total_lost').execute()
        total_bets = sum(u['total_bets'] for u in stats_response.data)
        total_won = sum(u['total_won'] for u in stats_response.data)
        total_lost = sum(u['total_lost'] for u in stats_response.data)
        
        return {
            'total_users': total_users,
            'total_bets': total_bets,
            'total_won': total_won,
            'total_lost': total_lost
        }
    except Exception as e:
        logger.error(f"Error getting bot stats: {e}")
        return {}


async def get_all_user_ids() -> List[int]:
    """Get all user IDs for broadcast"""
    try:
        response = supabase.table('users').select('id').execute()
        return [user['id'] for user in response.data]
    except Exception as e:
        logger.error(f"Error getting all user IDs: {e}")
        return []
