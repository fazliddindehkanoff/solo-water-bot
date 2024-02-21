from aiogram import types
from tgbot.bot.loader import dp


@dp.callback_query_handler(lambda callback_query: callback_query.data == "stats")
async def statistics_handler(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer("Test")


@dp.callback_query_handler(lambda callback_query: callback_query.data == "send_ads")
async def receive_ad_content_handler(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer("Test")


@dp.callback_query_handler(lambda callback_query: callback_query.data == "bonus_stats")
async def bonus_stats_handler(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer("Test")
