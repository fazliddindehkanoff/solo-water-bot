from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

back_to_courier_menu_inline_btn = InlineKeyboardMarkup()
back_to_courier_menu_inline_btn.add(
    InlineKeyboardButton("🔙 Ortga", callback_data="back_to_courier_menu")
)
