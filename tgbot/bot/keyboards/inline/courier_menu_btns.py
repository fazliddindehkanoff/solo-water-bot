from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from tgbot.constants import COUIRER_MAIN_MENU_BTNS


def courier_main_menu_btns() -> InlineKeyboardMarkup:
    main_menu_btns = InlineKeyboardMarkup(row_width=2)
    for callback_data, title in COUIRER_MAIN_MENU_BTNS.items():
        main_menu_btns.insert(InlineKeyboardButton(title, callback_data=callback_data))

    return main_menu_btns
