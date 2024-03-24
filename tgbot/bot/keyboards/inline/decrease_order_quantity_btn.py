from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def generate_quantity_buttons(current_quantity: int, order_id: int):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(
            f"Suv kapsulalari soni: {current_quantity}", callback_data="dummy"
        ),
        InlineKeyboardButton("-", callback_data=f"decrease_quantity:{order_id}"),
        InlineKeyboardButton(
            "🏁 Buyurtma yakunlandi", callback_data=f"order_finished:{order_id}"
        ),
    )
    return keyboard
