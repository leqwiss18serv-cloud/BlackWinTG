from functools import wraps
from aiogram import types
from aiogram.filters import Filter
import database


class OwnerOnly(Filter):
    """Filter for owner-only commands"""
    async def __call__(self, message: types.Message) -> bool:
        user = await database.get_user(message.from_user.id)
        return user and user['role'] == 'owner'


class AdminOnly(Filter):
    """Filter for admin and owner commands"""
    async def __call__(self, message: types.Message) -> bool:
        user = await database.get_user(message.from_user.id)
        return user and user['role'] in ['admin', 'owner']


class NotBanned(Filter):
    """Filter to check if user is not banned"""
    async def __call__(self, message: types.Message) -> bool:
        user = await database.get_user(message.from_user.id)
        return user and not user['is_banned']


def owner_only(func):
    """Decorator for owner-only handlers"""
    @wraps(func)
    async def wrapper(message: types.Message, *args, **kwargs):
        user = await database.get_user(message.from_user.id)
        if not user or user['role'] != 'owner':
            await message.answer("⛔ Эта команда доступна только владельцу бота")
            return
        return await func(message, *args, **kwargs)
    return wrapper


def admin_only(func):
    """Decorator for admin and owner handlers"""
    @wraps(func)
    async def wrapper(message: types.Message, *args, **kwargs):
        user = await database.get_user(message.from_user.id)
        if not user or user['role'] not in ['admin', 'owner']:
            await message.answer("⛔ Эта команда доступна только администраторам")
            return
        return await func(message, *args, **kwargs)
    return wrapper


def not_banned(func):
    """Decorator to check if user is not banned"""
    @wraps(func)
    async def wrapper(message: types.Message, *args, **kwargs):
        user = await database.get_user(message.from_user.id)
        if not user:
            await message.answer("❌ Пользователь не найден. Используйте /start")
            return
        if user['is_banned']:
            reason = user.get('ban_reason', 'Не указана')
            await message.answer(f"🚫 Вы заблокированы\n\n📝 Причина: {reason}")
            return
        return await func(message, *args, **kwargs)
    return wrapper
