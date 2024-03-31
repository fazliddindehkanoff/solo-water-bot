from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

bonus_btns = InlineKeyboardMarkup()
bonus_btns.add(
    InlineKeyboardButton(
        "🔄 Bonuslarni almashtirish", callback_data="proceed_exchange_bonus"
    )
)
bonus_btns.add(InlineKeyboardButton("🔙 Ortga", callback_data="back_to_bonuses_menu"))
