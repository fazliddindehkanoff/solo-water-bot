from aiogram import types
from tgbot.bot.loader import dp
from tgbot.bot.states.personal_data import PersonalDataStates
from tgbot.selectors import get_state
from tgbot.services import forward_post_to_all_users, set_state
from tgbot.bot.keyboards import (
    admins_main_menu_btns,
    admin_back_to_main_menu_inline_btn,
)


@dp.callback_query_handler(lambda callback_query: callback_query.data == "stats")
async def statistics_handler(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer("Test")


@dp.callback_query_handler(lambda callback_query: callback_query.data == "send_ads")
async def receive_ad_content_handler(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await callback_query.message.delete()
    set_state(user_id, "awaiting_post_content")

    await callback_query.message.answer(
        "Iltimos, barcha foydalanuvchilarga jo'natmoqchi bo'lgan habarni matn va mediya (rasm yoki video) bilan yozing:",
        reply_markup=admin_back_to_main_menu_inline_btn,
    )


@dp.message_handler(
    lambda message: get_state(message.chat.id) == "awaiting_post_content",
    content_types=["text", "photo", "video"],
)
async def forward_post_to_users(message: types.Message):
    user_id = message.chat.id
    await forward_post_to_all_users(message)
    set_state(user_id, "none")
    await message.answer(
        "Post barcha foydalanuvchilarga muvaffaqiyatli yuborildi!",
        reply_markup=admins_main_menu_btns,
    )


@dp.callback_query_handler(lambda callback_query: callback_query.data == "bonus_stats")
async def bonus_stats_handler(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer("Test")
