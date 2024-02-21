from aiogram import types

from tgbot.bot.keyboards import phone_number_btn, generate_subscription_btns
from tgbot.bot.loader import dp
from tgbot.bot.states import PersonalDataStates
from tgbot.selectors import get_state, get_subscriptions_info
from tgbot.services import set_state, set_user_data


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
