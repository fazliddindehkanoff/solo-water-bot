from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def generate_order_btns(order_id: int) -> InlineKeyboardMarkup:
    result = InlineKeyboardMarkup(row_width=2)
    result.insert(
        InlineKeyboardButton(
            "✅ Qabul qilish", callback_data=f"accept_order:{order_id}"
        )
    )
    result.insert(
        InlineKeyboardButton("❌ Rad etish", callback_data=f"decline_order:{order_id}")
    )
    return result


def generate_order_on_way_btn(order_id: int) -> InlineKeyboardMarkup:
    result = InlineKeyboardMarkup()
    result.insert(
        InlineKeyboardButton(
            "✅ Buyurtma yo'lga chiqdi", callback_data=f"order_on_the_way:{order_id}"
        )
    )
    return result


def generate_finish_order_btn(order_id: int) -> InlineKeyboardMarkup:
    result = InlineKeyboardMarkup()
    result.insert(
        InlineKeyboardButton(
            "🏁 Buyurtma yakunlandi", callback_data=f"order_finished:{order_id}"
        )
    )
    return result
