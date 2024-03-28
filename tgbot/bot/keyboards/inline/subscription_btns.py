from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from tgbot.constants import NUM_EMOJIS


def generate_subscription_btns(
    subscription_ids: list, renew=False
) -> InlineKeyboardMarkup:
    subscription_btns = InlineKeyboardMarkup(row_width=5)
    for index, id in enumerate(subscription_ids, start=1):
        callback_data = f"renew:subscription:{id}" if renew else f"subscription:{id}"
        subscription_btns.insert(
            InlineKeyboardButton(
                f"{NUM_EMOJIS.get(index)}", callback_data=callback_data
            )
        )

    return subscription_btns
