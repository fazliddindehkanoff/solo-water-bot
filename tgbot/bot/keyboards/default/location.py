from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

location_btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
btn = KeyboardButton("📍 Manzilni tasdiqlash", request_location=True)
location_btn.add(btn)
