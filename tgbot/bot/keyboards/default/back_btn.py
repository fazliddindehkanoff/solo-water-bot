from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

back_to_main_menu_bnt = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
)
back_to_main_menu_bnt.add(KeyboardButton("🔙 Ortga"))
