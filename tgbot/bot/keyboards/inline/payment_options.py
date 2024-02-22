from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

payment_option_btns = InlineKeyboardMarkup(row_width=2)
card_option = InlineKeyboardButton("💳 Karta orqali", callback_data="payment_by:1")
cash_option = InlineKeyboardButton("💴 Naqd pul orqali", callback_data="payment_by:2")
payment_option_btns.insert(card_option)
payment_option_btns.insert(cash_option)
