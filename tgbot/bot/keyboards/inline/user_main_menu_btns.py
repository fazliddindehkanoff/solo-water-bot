from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.constants import MAIN_MENU_BTNS


def generate_menu_btns(btns: dict = MAIN_MENU_BTNS) -> InlineKeyboardMarkup:
    menu_btns = InlineKeyboardMarkup(row_width=2)
    current_row = []
    for callback_data, title in btns.items():
        if callback_data.startswith("nr:"):
            callback_data = callback_data[3:]  # Remove "nr:" prefix
            if current_row:
                menu_btns.add(*current_row)
                current_row = []
        current_row.append(
            InlineKeyboardButton(
                title,
                callback_data=callback_data,
            )
        )

    if current_row:
        menu_btns.add(*current_row)

    return menu_btns
