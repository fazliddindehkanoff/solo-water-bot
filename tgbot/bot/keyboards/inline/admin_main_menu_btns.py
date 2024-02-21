from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

admins_main_menu_btns = InlineKeyboardMarkup(row_width=2)
stats = InlineKeyboardButton("📊 Statistika", callback_data="stats")
send_ads = InlineKeyboardButton("📬 Habar yuborish", callback_data="send_ads")
bonus_stats = InlineKeyboardButton(
    "🧮 Foydalanuvchilar bonusi", callback_data="bonus_stats"
)
admins_main_menu_btns.add(stats)
admins_main_menu_btns.add(send_ads)
admins_main_menu_btns.add(bonus_stats)
