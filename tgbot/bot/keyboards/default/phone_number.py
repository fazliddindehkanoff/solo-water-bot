from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

phone_number_btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
btn = KeyboardButton("📲 Tasdiqlash", request_contact=True)
phone_number_btn.add(btn)
