from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_back_to_main_menu_inline_btn = InlineKeyboardMarkup()
admin_back_to_main_menu_inline_btn.add(
    InlineKeyboardButton("🔙 Ortga", callback_data="admin_back_to_main_menu")
)
