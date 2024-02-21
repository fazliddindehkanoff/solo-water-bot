from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from tgbot.bot.loader import dp
from tgbot.bot.states import PersonalDataStates
from tgbot.services import register_user
from tgbot.selectors import get_state
from tgbot.services import set_state


# Define command handlers
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        user_id = message.chat.id
        role = register_user(user_id=user_id)
        greetings = {
            1: f"Assalomu alaykum Xo'jayin, {message.from_user.full_name}!",
            2: f"Assalomu alaykum, Admin, {message.from_user.full_name}!",
            3: f"Salom, {message.from_user.full_name}!",
        }
        if role == 3:
            greetings[
                3
            ] += "\nBotimizga xush kelibsiz, Iltimos to'liq ismingizni kiriting:"
            set_state(user_id, PersonalDataStates.FULL_NAME)

        await message.answer(greetings.get(role, "Salom!"))
    except Exception as e:
        print(e)
