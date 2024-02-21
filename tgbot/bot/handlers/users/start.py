from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from tgbot.bot.loader import dp
from tgbot.bot.states import PersonalDataStates
from tgbot.bot.keyboards import admins_main_menu_btns
from tgbot.services import register_user
from tgbot.selectors import get_state
from tgbot.services import set_state


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        user_id = message.chat.id
        role = register_user(user_id=user_id)

        if role == 1:
            await message.answer(
                text="Assalomu alaykum 🤖\nXo'jayin xush kelibsiz",
                reply_markup=admins_main_menu_btns,
            )

        elif role == 2:
            set_state(user_id, PersonalDataStates.FULL_NAME)
            await message.answer(
                f"Assalomu alaykum {message.from_user.full_name}\nBotimizga xush kelibsiz, Iltimos to'liq ismingizni kiriting:"
            )

    except Exception as e:
        print(e)
