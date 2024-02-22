from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from tgbot.bot.loader import dp
from tgbot.bot.keyboards import (
    admins_main_menu_btns,
    registration_option_btns,
    generate_main_menu_btns,
)
from tgbot.services import create_referal, register_user


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    command_args = message.get_args()
    user_id = message.chat.id
    role, exists = register_user(user_id=user_id)
    main_menu_btns = generate_main_menu_btns()

    if role == 1:
        await message.answer(
            text="Assalomu alaykum 🤖\nXo'jayin xush kelibsiz",
            reply_markup=admins_main_menu_btns,
        )

    elif role == 2:
        if exists:
            await message.answer("Asosiy menu", reply_markup=main_menu_btns)
        else:
            if command_args:
                create_referal(message.from_user.id, command_args)
            await message.answer(
                f"Assalomu alaykum {message.from_user.full_name}\nBotimizga xush kelibsiz, Ro'yxatdan o'tish turini tanlang",
                reply_markup=registration_option_btns,
            )
