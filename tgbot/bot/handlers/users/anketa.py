from aiogram import types

from tgbot.bot.loader import dp
from tgbot.bot.states import PersonalDataStates
from tgbot.selectors import get_state
from tgbot.services import set_state, set_user_data


# /form komandasi uchun handler yaratamiz. Bu yerda foydalanuvchi hech qanday holatda emas, state=None


@dp.message_handler(
    lambda message: get_state(message.from_user.id) == PersonalDataStates.FULL_NAME
)
async def answer_full_name(message: types.Message):
    user_id = message.chat.id
    full_name = message.text
    try:
        set_user_data(user_id, "full_name", full_name)
        await message.answer("Telefon raqamingizni kiriting")
        set_state(user_id, PersonalDataStates.PHONE_NUMBER)
    except Exception as e:
        await message.answer(str(e))


@dp.message_handler(
    lambda message: get_state(message.from_user.id) == PersonalDataStates.PHONE_NUMBER
)
async def answer_phone(message: types.Message):
    user_id = message.chat.id
    phone_number = message.text
    set_user_data(user_id, "phone_number", phone_number)
    await message.answer(
        "Suv yetkazilishi kerak bo'lgan manzilni yuboring(location formatida)"
    )
    set_state(user_id, PersonalDataStates.LOCATION)


@dp.message_handler(
    lambda message: get_state(message.from_user.id) == PersonalDataStates.LOCATION
)
async def answer_location(message: types.Message):
    phone = message.text
    await message.answer("Hello world")
    print("finished")
