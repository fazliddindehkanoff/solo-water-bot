from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

registration_option_btns = InlineKeyboardMarkup()
register = InlineKeyboardButton("Ro'yxatdan o'tish", callback_data="register")
register_by_operator = InlineKeyboardButton(
    "Operator orqali ro'yxatdan o'tish", callback_data="register_by_operator"
)
registration_option_btns.add(register)
registration_option_btns.add(register_by_operator)
