from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

back_to_main_menu_inline_btn = InlineKeyboardMarkup()
back_to_main_menu_inline_btn.add(
    InlineKeyboardButton("🔙 Ortga", callback_data="back_to_main_menu")
)


back_to_bonuses_menu_inline_btn = InlineKeyboardMarkup()
back_to_bonuses_menu_inline_btn.add(
    InlineKeyboardButton("🔙 Ortga", callback_data="back_to_bonuses_menu")
)
