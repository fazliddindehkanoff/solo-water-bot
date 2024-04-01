from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from tgbot.constants import NUM_EMOJIS


def generate_subscription_btns(
    subscription_ids: list, renew=False
) -> InlineKeyboardMarkup:
    subscription_btns = InlineKeyboardMarkup(row_width=5)
    callback_suffix = "renew:" if renew else ""
    for index, id in enumerate(subscription_ids, start=1):
        subscription_btns.insert(
            InlineKeyboardButton(
                f"{NUM_EMOJIS.get(index)}",
                callback_data=f"{callback_suffix}subscription:{id}",
            )
        )
    subscription_btns.add(
        InlineKeyboardButton(
            "Donalab buyurtma berish",
            callback_data=f"{callback_suffix}without_subscription",
        )
    )

    return subscription_btns
