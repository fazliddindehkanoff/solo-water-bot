from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from tgbot.constants import NUM_EMOJIS


def generate_subscription_btns(subscription_ids: list) -> InlineKeyboardMarkup:
    subscription_btns = InlineKeyboardMarkup(row_width=5)
    for index, id in enumerate(subscription_ids, start=1):
        subscription_btns.insert(
            InlineKeyboardButton(
                f"{NUM_EMOJIS.get(index)}", callback_data=f"subscription:{id}"
            )
        )

    return subscription_btns
