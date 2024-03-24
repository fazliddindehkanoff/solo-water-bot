from aiogram import types

from tgbot.bot.states import CourierRegistrationStates
from tgbot.bot.keyboards import (
    back_to_courier_menu_inline_btn,
    courier_main_menu_btns,
    generate_order_on_way_btn,
    generate_finish_order_btn,
    generate_main_menu_btns,
    phone_number_btn,
    generate_quantity_buttons,
)
from tgbot.bot.loader import dp, bot
from tgbot.selectors import (
    get_client_chat_id,
    get_courier_details_formatted,
    get_curier_data,
    get_finished_orders_details,
    get_order_notification_text,
    get_state,
)
from tgbot.services import (
    decrease_order_and_get_quantity,
    remove_kurier_from_order,
    set_courier_data,
    set_state,
    update_order_status,
)

ORDERS_CHANNEL = "-1002018856872"


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == "courier_details"
)
async def courier_details(callback_query: types.CallbackQuery):
    curier_details = get_courier_details_formatted(user_id=callback_query.from_user.id)
    await callback_query.message.delete()
    await callback_query.message.answer(
        f"Sizning ma'lumotlaringiz: \n\n{curier_details}",
        reply_markup=back_to_courier_menu_inline_btn,
    )


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == "history_of_orders"
)
async def history_of_products(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    order_details = get_finished_orders_details(user_id=callback_query.from_user.id)
    await callback_query.message.answer(
        f"Sizning buyurtmalar tarixingiz: \n\n{order_details}",
        reply_markup=back_to_courier_menu_inline_btn,
    )


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == "courier_contact_with_operator"
)
async def contact_with_operator(callback_query: types.CallbackQuery):
    curier_data = get_curier_data(chat_id=callback_query.from_user.id)

    await callback_query.message.delete()
    await bot.send_message(
        chat_id=ORDERS_CHANNEL,
        text=f"Ushbu kurier bilan aloqaga chiqish zarur!\n\n{curier_data}\n\n#aloqa #operator_yordami",
    )
    await callback_query.message.answer(
        "So'rovingiz yuborildi, tez orada siz bilan aloqaga chiqamiz",
        reply_markup=courier_main_menu_btns(),
    )


@dp.callback_query_handler(
    lambda callback_query: callback_query.data.startswith("decline_order")
)
async def decline_order(callback_query: types.CallbackQuery):
    curier_data = get_curier_data(chat_id=callback_query.from_user.id)
    order_id = callback_query.data.split(":")[-1]
    remove_kurier_from_order(order_id=order_id)

    await callback_query.message.delete()
    await bot.send_message(
        chat_id=ORDERS_CHANNEL,
        text=f"Ushbu kurier #{order_id} lik buyurtmani qabul qilmadi!\n\n{curier_data}\n\nIltimos ushbu buyurtma uchun qaytadan kurier biriktiring.",
    )
    await callback_query.message.answer(
        "Buyurtma sizdan boshqa kurierga olindi",
        reply_markup=courier_main_menu_btns(),
    )


@dp.callback_query_handler(
    lambda callback_query: callback_query.data.startswith("accept_order")
)
async def accept_order(callback_query: types.CallbackQuery):
    order_id = callback_query.data.split(":")[-1]

    await callback_query.message.delete()
    await callback_query.message.answer(
        "Endi yukni olib yo'lga chiqgan paytda quyidagi tugma orqali yo'lga chiqganingizni tasdiqlab qo'ying",
        reply_markup=generate_order_on_way_btn(order_id=order_id),
    )


@dp.callback_query_handler(
    lambda callback_query: callback_query.data.startswith("order_on_the_way")
)
async def order_on_the_way(callback_query: types.CallbackQuery):
    order_id = callback_query.data.split(":")[-1]
    _message, chat_id = get_order_notification_text(order_id=order_id)
    curier_data = get_curier_data(chat_id=callback_query.from_user.id)
    message = f"{_message}\nKurier ma'lumotlari: \n\n{curier_data}"
    update_order_status(order_id, 4)

    await callback_query.message.delete()
    await callback_query.message.answer(
        "Endi yukni yetkazib bo'lgandan so'ng quyidagi tugma orqali buyurtma yakunlanganligini tasdiqlab qo'ying",
        reply_markup=generate_finish_order_btn(order_id=order_id),
    )
    await bot.send_message(chat_id=chat_id, text=message)


@dp.callback_query_handler(
    lambda callback_query: callback_query.data.startswith("decrease_quantity")
)
async def decrease_quantity(callback_query: types.CallbackQuery):
    order_id = callback_query.data.split(":")[-1]
    order_quantity = decrease_order_and_get_quantity(order_id=order_id)
    keyboard = generate_quantity_buttons(order_quantity, order_id)
    await callback_query.message.delete()
    await callback_query.message.answer(
        "Buyurtma qilingan mahsulotni kamaytiring:", reply_markup=keyboard
    )


@dp.callback_query_handler(
    lambda callback_query: callback_query.data.startswith("minimiz_order")
)
async def minimize_order(callback_query: types.CallbackQuery):
    print("order_id")
    order_id = callback_query.data.split(":")[-1]
    order_quantity = decrease_order_and_get_quantity(order_id=order_id, decrease=False)
    keyboard = generate_quantity_buttons(order_quantity, order_id)
    await callback_query.message.delete()
    await callback_query.message.answer(
        "Buyurtma qilingan mahsulotni kamaytiring:", reply_markup=keyboard
    )


@dp.callback_query_handler(
    lambda callback_query: callback_query.data.startswith("order_finished")
)
async def finish_order(callback_query: types.CallbackQuery):
    order_id = callback_query.data.split(":")[-1]
    chat_id = get_client_chat_id(order_id=order_id)
    update_order_status(order_id=order_id, status=2)

    await callback_query.message.delete()
    await callback_query.message.answer(
        "Buyurtma muvaffaqiyatli yakunlandi!",
        reply_markup=courier_main_menu_btns(),
    )
    await bot.send_message(
        chat_id=chat_id,
        text="Buyurtmangiz muvaffaqiyatli yetkazildi, agar bu habar no to'g'ri bo'lsa, iltimos operatorlarimizga habar bering",
    )
    await bot.send_message(
        chat_id=chat_id,
        text="asosiy menu",
        reply_markup=generate_main_menu_btns(),
    )


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == "back_to_courier_menu"
)
async def back_to_main_menu(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer(
        "Asosiy menu", reply_markup=courier_main_menu_btns()
    )


@dp.message_handler(
    lambda message: get_state(message.from_user.id)
    == CourierRegistrationStates.FULL_NAME
)
async def answer_courier_full_name(message: types.Message):
    user_id = message.chat.id
    full_name = message.text
    try:
        set_courier_data(user_id, "full_name", full_name)
        await message.answer(
            "Iltimos, telefon raqamingizni tasdiqlang:", reply_markup=phone_number_btn
        )
        set_state(user_id, CourierRegistrationStates.PHONE_NUMBER)
    except Exception as e:
        await message.answer(str(e))


@dp.message_handler(
    lambda message: get_state(message.from_user.id)
    == CourierRegistrationStates.PHONE_NUMBER,
    content_types=["contact", "text"],
)
async def answer_courier_phone(message: types.Message):
    user_id = message.chat.id
    try:
        phone_number = message.contact.phone_number
    except Exception:
        await message.answer(
            "Iltimos, telefon raqamingizni quyidagi tugma orqali tasdiqlang:",
            reply_markup=phone_number_btn,
        )
        return
    set_courier_data(user_id, "phone_number", str(phone_number))
    await message.answer(
        "Iltimos, tug'ulgan sanangizni ushbu formatda kiriting: (yil-oy-kun)",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    set_state(user_id, CourierRegistrationStates.BIRTH_DATE)


@dp.message_handler(
    lambda message: get_state(message.from_user.id)
    == CourierRegistrationStates.BIRTH_DATE,
    content_types=["text"],
)
async def answer_courier_birth_date(message: types.Message):
    user_id = message.chat.id
    birth_date = message.text
    try:
        set_courier_data(user_id, "birth_date", birth_date)
        await message.answer(
            "Iltimos, pasport ma'lumotlaringizni ushbu tartibda kiriting (AB 1234567):"
        )
        set_state(user_id, CourierRegistrationStates.PASSPORT_DATA)
    except Exception as e:
        await message.answer(str(e))


@dp.message_handler(
    lambda message: get_state(message.from_user.id)
    == CourierRegistrationStates.PASSPORT_DATA,
    content_types=["text"],
)
async def answer_courier_passport_data(message: types.Message):
    user_id = message.chat.id
    passport_data = message.text
    try:
        set_courier_data(user_id, "passport_data", passport_data)
        await message.answer("Iltimos, manzilingizni yuboring:")
        set_state(user_id, CourierRegistrationStates.ADDRESS)
    except Exception as e:
        await message.answer(str(e))


@dp.message_handler(
    lambda message: get_state(message.from_user.id)
    == CourierRegistrationStates.ADDRESS,
    content_types=["text"],
)
async def answer_courier_address(message: types.Message):
    user_id = message.chat.id
    address = message.text
    try:
        set_courier_data(user_id, "address", address)
        await message.answer("Iltimos, ikkinchi telefon raqamingizni kiriting:")
        set_state(user_id, CourierRegistrationStates.PHONE_NUMBERS_2)
    except Exception as e:
        await message.answer(str(e))


@dp.message_handler(
    lambda message: get_state(message.from_user.id)
    == CourierRegistrationStates.PHONE_NUMBERS_2,
    content_types=["text"],
)
async def answer_courier_phone_numbers_2(message: types.Message):
    user_id = message.chat.id
    phone_numbers_2 = message.text
    try:
        set_courier_data(user_id, "phone_numbers_2", phone_numbers_2)
        await message.answer("Iltimos, mashinangizning rusumini kiriting:")
        set_state(user_id, CourierRegistrationStates.CAR_MODEL)
    except Exception as e:
        await message.answer(str(e))


@dp.message_handler(
    lambda message: get_state(message.from_user.id)
    == CourierRegistrationStates.CAR_MODEL,
    content_types=["text"],
)
async def answer_courier_car_model(message: types.Message):
    user_id = message.chat.id
    car_model = message.text
    try:
        set_courier_data(user_id, "car_model", car_model)
        await message.answer("Iltimos, mashinangizning davlat raqamini kiriting:")
        set_state(user_id, CourierRegistrationStates.CAR_LICENSE_PLATE)
    except Exception as e:
        await message.answer(str(e))


@dp.message_handler(
    lambda message: get_state(message.from_user.id)
    == CourierRegistrationStates.CAR_LICENSE_PLATE,
    content_types=["text"],
)
async def answer_courier_car_license_plate(message: types.Message):
    user_id = message.chat.id
    car_license_plate = message.text
    try:
        set_courier_data(user_id, "car_license_plate", car_license_plate)
        await message.answer(
            "Tabriklaymiz! Ro'yxatdan o'tish muvaffaqiyatli yakunlandi.",
            reply_markup=courier_main_menu_btns(),
        )
    except Exception as e:
        await message.answer(str(e))
