from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

admins_main_menu_btns = InlineKeyboardMarkup(row_width=2)
stats = InlineKeyboardButton("📊 Statistika", callback_data="stats")
send_ads = InlineKeyboardButton("📬 Habar yuborish", callback_data="send_ads")
bonus_stats = InlineKeyboardButton(
    "🧮 Foydalanuvchilar bonusi", callback_data="bonus_stats"
)
curier_referal = InlineKeyboardButton(
    "🏃‍♂️ Kurier uchun referal link", callback_data="get_link_for_curier"
)
admins_main_menu_btns.insert(stats)
admins_main_menu_btns.insert(send_ads)
admins_main_menu_btns.insert(bonus_stats)
admins_main_menu_btns.insert(curier_referal)
