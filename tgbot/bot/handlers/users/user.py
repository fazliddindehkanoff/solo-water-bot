from aiogram import types

from tgbot.bot.keyboards import (
    phone_number_btn,
    generate_subscription_btns,
    payment_option_btns,
)
from tgbot.bot.loader import dp
from tgbot.bot.states import PersonalDataStates
from tgbot.selectors import get_state, get_subscriptions_info
from tgbot.services import set_state, set_user_data


@dp.callback_query_handler(lambda callback_query: callback_query.data == "register")
async def ask_full_name(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    set_state(user_id, PersonalDataStates.FULL_NAME)

    await callback_query.message.delete()
    await callback_query.message.answer("Iltimos to'liq ismingizni kiriting:")


@dp.message_handler(
    lambda message: get_state(message.from_user.id) == PersonalDataStates.FULL_NAME
)
async def answer_full_name(message: types.Message):
    user_id = message.chat.id
    full_name = message.text
    try:
        set_user_data(user_id, "full_name", full_name)
        await message.answer(
            "Telefon raqamingizni kiriting", reply_markup=phone_number_btn
        )
        set_state(user_id, PersonalDataStates.PHONE_NUMBER)
    except Exception as e:
        await message.answer(str(e))


@dp.message_handler(
    lambda message: get_state(message.from_user.id) == PersonalDataStates.PHONE_NUMBER,
    content_types=["contact"],
)
async def answer_phone(message: types.Message):
    user_id = message.chat.id
    phone_number = message.contact.phone_number

    if not phone_number:
        await message.answer(
            "Iltimos, telefon raqamingizni jo'nating yoki kontaktni yuboring.",
            reply_markup=phone_number_btn,
        )
        return
    set_user_data(user_id, "phone_number", str(phone_number))
    await message.answer(
        "Suv yetkazilishi kerak bo'lgan manzilni yuboring",
    )
    set_state(user_id, PersonalDataStates.LOCATION)


@dp.message_handler(
    lambda message: get_state(message.from_user.id) == PersonalDataStates.LOCATION
)
async def answer_location(message: types.Message):
    user_id = message.chat.id
    address = message.text
    text, subscription_ids = get_subscriptions_info()
    subscription_btns = generate_subscription_btns(subscription_ids)
    set_user_data(user_id, "address", address)
    await message.answer(
        f"ℹ️ Tariflarimiz haqida ma'lumotlar:\n\n{text}Iltimos o'zingizga qulay bo'lgan ta'rif tanlang: ",
        reply_markup=subscription_btns,
    )


@dp.callback_query_handler(
    lambda callback_query: callback_query.data.startswith("subscription")
)
async def set_subscription(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    subscription_id = callback_query.data.split(":")[-1]
    set_user_data(user_id, "subscription_id", subscription_id)
    await callback_query.message.delete()
    await callback_query.message.answer(
        "To'lov turini tanlang: ", reply_markup=payment_option_btns
    )


@dp.callback_query_handler(
    lambda callback_query: callback_query.data.startswith("payment_by")
)
async def set_payment_type(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    payment_type = callback_query.data.split(":")[-1]
    set_user_data(user_id, "payment_type", payment_type)
    await callback_query.message.delete()
    await callback_query.message.answer("Asosiy menu")
