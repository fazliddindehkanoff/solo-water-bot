from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.constants import NUM_EMOJIS
from tgbot.models import Promotion


def get_promotions() -> tuple[str, InlineKeyboardMarkup]:
    data = ""
    promotion_btn = InlineKeyboardMarkup(row_width=3)
    promotions = Promotion.objects.all()
    for index, promotion in enumerate(promotions, start=1):
        promotion_btn.insert(
            InlineKeyboardButton(
                text=NUM_EMOJIS[index],
                callback_data=f"exchange_bonus_by:{promotion.pk}",
            )
        )
        data += f"{NUM_EMOJIS[index]} {promotion.number_of_stars} ball uchun {promotion.winning_price:,} so'm yutuq\n"

    promotion_btn.add(
        InlineKeyboardButton("🔙 Ortga", callback_data="back_to_main_menu")
    )
    return data, promotion_btn
