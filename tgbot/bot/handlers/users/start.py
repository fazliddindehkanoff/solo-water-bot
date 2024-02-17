from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from tgbot.models import TelegramUser
from tgbot.bot.loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    TelegramUser.objects.create(chat_id=message.chat.id)
    await message.answer(f"Salom, {message.from_user.full_name}!")
