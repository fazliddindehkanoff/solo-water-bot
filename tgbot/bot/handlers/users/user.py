from aiogram import types

from tgbot.bot.keyboards import (
    phone_number_btn,
    generate_subscription_btns,
    payment_option_btns,
    generate_menu_btns,
    back_to_main_menu_inline_btn,
    bonus_btns,
    back_to_bonuses_menu_inline_btn,
)
from tgbot.bot.loader import dp, bot
from tgbot.bot.states import PersonalDataStates
from tgbot.selectors import (
    generate_referal_link,
    get_cliend_data,
    get_cliend_order_data,
    get_client_order_details,
    get_number_of_available_products,
    get_referralers_data,
    get_state,
    get_subscriptions_info,
    get_user_bonus,
    get_user_details,
    get_user_phone_number,
    get_user_subscription_status,
    is_user_active,
)
from tgbot.services import create_order, set_state, set_user_data
from tgbot.constants import BONUS_MENU_BTNS


ORDERS_CHANNEL = "-1002018856872"
REGISTRATION_CHANNEL = "-1002098130597"


@dp.callback_query_handler(lambda callback_query: callback_query.data == "register")
async def ask_full_name(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    set_state(user_id, PersonalDataStates.FULL_NAME)

    await callback_query.message.delete()
    await callback_query.message.answer("Iltimos to'liq ismingizni kiriting:")


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == "register_by_operator"
)
async def register_by_operator(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    set_state(user_id, PersonalDataStates.REGISTER_BY_OPERATOR)

    await callback_query.message.delete()
    await callback_query.message.answer(
        "Iltimos telefon raqamingizni tasdiqlang:", reply_markup=phone_number_btn
    )


@dp.message_handler(
    lambda message: get_state(message.from_user.id)
    == PersonalDataStates.REGISTER_BY_OPERATOR,
    content_types=["contact", "text"],
)
async def get_phone_num(message: types.Message):
    user_id = message.chat.id
    try:
        phone_number = message.contact.phone_number
    except Exception:
        await message.answer(
            "Iltimos, telefon raqamingizni quyidagi tugma orqali tasdiqlang!",
            reply_markup=phone_number_btn,
        )
        return
    set_user_data(user_id, "phone_number", str(phone_number))
    await message.answer(
        "Operatorlarimiz siz bilan tez orada aloqaga chiqishadi",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await bot.send_message(
        chat_id=REGISTRATION_CHANNEL,
        text=f"Yangi mijoz ro'yxatdan o'tish uchun operator yordamini so'radi:\nMijoz telefon raqami{phone_number}\n\n#yangi_mijoz #yordam #ro'yxatga_olish",
    )


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
    content_types=["contact", "text"],
)
async def answer_phone(message: types.Message):
    user_id = message.chat.id
    try:
        phone_number = message.contact.phone_number
    except Exception:
        await message.answer(
            "Iltimos, telefon raqamingizni quyidagi tugma orqali tasdiqlang!",
            reply_markup=phone_number_btn,
        )
        return
    set_user_data(user_id, "phone_number", str(phone_number))
    await message.answer(
        "Suv yetkazilishi kerak bo'lgan manzilni yuboring",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    set_state(user_id, PersonalDataStates.LOCATION)


@dp.message_handler(
    lambda message: get_state(message.from_user.id) == PersonalDataStates.LOCATION,
    content_types=["location", "text"],
)
async def answer_location(message: types.Message):
    user_id = message.chat.id
    if message.content_type == "location":
        await message.answer("Iltimos manzilni habar ko'rinishida yuboring.")
    else:
        address = message.text
        text, subscription_ids = get_subscriptions_info()
        subscription_btns = generate_subscription_btns(subscription_ids)
        set_user_data(user_id, "address", address)
        await message.answer(
            f"ℹ️ Tariflarimiz haqida ma'lumotlar:\n\n{text}Iltimos o'zingizga qulay bo'lgan ta'rif tanlang: ",
            reply_markup=subscription_btns,
        )


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == "subscriptions"
)
async def list_of_subscriptions(callback_query: types.CallbackQuery):
    text, _ = get_subscriptions_info()
    await callback_query.message.delete()
    await callback_query.message.answer(
        f"Tariflarimiz haqida ma'lumotlar: \n\n{text}",
        reply_markup=back_to_main_menu_inline_btn,
    )


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == "without_subscription"
)
async def set_without_subscription(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    set_user_data(user_id, "subscription_based", False)

    await callback_query.message.delete()
    await callback_query.message.answer(
        "To'lov turini tanlang: ", reply_markup=payment_option_btns
    )


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == "renew:without_subscription"
)
async def set_without_subscription(callback_query: types.CallbackQuery):
    print("TEST")
    user_id = callback_query.from_user.id
    set_user_data(user_id, "subscription_based", False)

    await callback_query.message.delete()
    await callback_query.message.answer(
        "Nechta kapsula buyurtma qilmoqchisiz?",
        reply_markup=back_to_main_menu_inline_btn,
    )


@dp.callback_query_handler(
    lambda callback_query: callback_query.data.startswith("subscription")
)
async def set_subscription(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    subscription_id = callback_query.data.split(":")[-1]

    if subscription_id != "0":
        set_user_data(user_id, "subscription", subscription_id)

    else:
        set_user_data(user_id, "subscription_based", False)

    await callback_query.message.delete()
    await callback_query.message.answer(
        "To'lov turini tanlang: ", reply_markup=payment_option_btns
    )


@dp.callback_query_handler(
    lambda callback_query: callback_query.data.startswith("renew:subscription")
)
async def renew_subscription(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    subscription_id = callback_query.data.split(":")[-1]
    set_user_data(user_id, "subscription", subscription_id)

    await callback_query.message.delete()
    await callback_query.message.answer(
        f"Yangi tarifingiz aktivlashdi, nechta kapsulada maxsulot buyurtma qilmoqchisiz? ",
        reply_markup=back_to_main_menu_inline_btn,
    )
    set_state(user_id, PersonalDataStates.GET_ORDER)


@dp.callback_query_handler(
    lambda callback_query: callback_query.data.startswith("payment_by")
)
async def set_payment_type(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    payment_type = callback_query.data.split(":")[-1]
    menu_btns = generate_menu_btns()
    set_user_data(user_id, "payment_type", payment_type)
    await callback_query.message.delete()
    client_data = get_cliend_data(user_id)
    await bot.send_message(
        chat_id=REGISTRATION_CHANNEL,
        text=f"Yangi mijoz ro'yxatdan o'tdi, Mijoz ma'lumotlar:\n{client_data}\n\n#yangi_mijoz",
    )
    await callback_query.message.answer("Asosiy menu", reply_markup=menu_btns)


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == "contact_with_operator"
)
async def contact_operators(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    menu_btns = generate_menu_btns()

    await callback_query.message.delete()
    client_data = get_cliend_data(user_id)
    await bot.send_message(
        chat_id=ORDERS_CHANNEL,
        text=f"Ushbu mijozimizga aloqaga chiqish zarur!\n{client_data}\n\n#aloqa #operator_yordami",
    )
    await callback_query.message.answer(
        "So'rovingiz operatorlarimizga yuborildi, tez orada siz bilan aloqaga chiqishadi",
        reply_markup=menu_btns,
    )


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == "my_referal_link"
)
async def get_referal_link(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await callback_query.message.delete()
    await callback_query.message.answer(
        f"Sizning referal linkingiz: {generate_referal_link(user_id)}\n ko'proq tanishlaringizni botimizga jalb qiling va qimmatbaho sovg'alarga ega bo'ling!",
        reply_markup=back_to_bonuses_menu_inline_btn,
    )


@dp.callback_query_handler(lambda callback_query: callback_query.data == "my_referals")
async def get_referralers(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    data = get_referralers_data(user_id)
    user_bonuses = get_user_bonus(chat_id=user_id)
    await callback_query.message.delete()

    if len(data) != 0:
        await callback_query.message.answer(
            f"Bonus ballaringiz:{user_bonuses}\nSiz taklif qilgan foydalanuvchilar 👇:\n{data}",
            reply_markup=back_to_bonuses_menu_inline_btn,
        )
    else:
        await callback_query.message.answer(
            f"Siz hali hech kimni taklif qilmagansiz!",
            reply_markup=back_to_bonuses_menu_inline_btn,
        )


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == "back_to_bonuses_menu"
)
async def back_to_bonuses_menu(callback_query: types.CallbackQuery):
    menu_btns = generate_menu_btns(BONUS_MENU_BTNS)
    await callback_query.message.delete()
    await callback_query.message.answer(
        "Bonuslar menusi",
        reply_markup=menu_btns,
    )


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == "back_to_main_menu"
)
async def back_to_main_menu_from_referalls(callback_query: types.CallbackQuery):
    menu_btns = generate_menu_btns()
    await callback_query.message.delete()
    await callback_query.message.answer(
        "Asosiy menu",
        reply_markup=menu_btns,
    )


@dp.callback_query_handler(lambda callback_query: callback_query.data == "order")
async def give_an_order(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_status = is_user_active(user_id)
    subscription_based = get_user_subscription_status(user_id)
    menu_btns = generate_menu_btns()
    number_of_available_products = get_number_of_available_products(user_id)

    await callback_query.message.delete()
    if subscription_based:
        if number_of_available_products == 0:
            text, subscription_ids = get_subscriptions_info()
            subscription_btns = generate_subscription_btns(subscription_ids, renew=True)
            await callback_query.message.answer(
                f"ℹ️ Siz tarifingiz bo'yicha barcha suv kapsulalarini qabul qilib bo'ldingiz, iltimos yangi tarif tanlang:\n\n{text}Iltimos o'zingizga qulay bo'lgan ta'rif tanlang: ",
                reply_markup=subscription_btns,
            )

        elif user_status and not number_of_available_products == 0:
            await callback_query.message.answer(
                f"Nechta kapsulada maxsulot buyurtma qilmoqchisiz? \nMaximum: {number_of_available_products}",
                reply_markup=back_to_main_menu_inline_btn,
            )
            set_state(user_id, PersonalDataStates.GET_ORDER)

        else:
            await callback_query.message.answer(
                "Sizning akkauntingiz hali aktivlashmagan adminlarimiz tez orada siz bilan bog'lanishadi!",
                reply_markup=menu_btns,
            )
    else:
        await callback_query.message.answer(
            f"Nechta kapsulada maxsulot buyurtma qilmoqchisiz?",
            reply_markup=back_to_main_menu_inline_btn,
        )
        set_state(user_id, PersonalDataStates.GET_ORDER)


@dp.message_handler(
    lambda message: get_state(message.from_user.id) == PersonalDataStates.GET_ORDER
)
async def get_number_of_order(message: types.Message):
    user_id = message.from_user.id
    order_number: str = message.text
    subscription_based = get_user_subscription_status(user_id)
    number_of_available_products = get_number_of_available_products(user_id)

    if not order_number.isdigit():
        await message.answer(
            "Iltimos faqat raqam yuboring", reply_markup=back_to_main_menu_inline_btn
        )

    elif not subscription_based:
        order_id = create_order(user_id, order_number)
        data = get_cliend_order_data(user_id, order_id, order_number)
        await bot.send_message(
            ORDERS_CHANNEL, f"Yangi buyurtma\n{data}\n\n#yangi_buyurtma"
        )
        await message.answer(
            "Buyurtmangiz qabul qilindi tez orada buyurtmangiz yetkaziladi",
            reply_markup=generate_menu_btns(),
        )

    else:
        order_number = int(order_number)
        if order_number > number_of_available_products:
            await message.answer(
                f"Eng ko'pi bilan {number_of_available_products} ta maxsulot buyurtma qilishingiz mumkin xolos, iltimos qaytadan urinib ko'ring",
                reply_markup=back_to_main_menu_inline_btn,
            )
        else:
            order_id = create_order(user_id, order_number)
            data = get_cliend_order_data(user_id, order_id, order_number)
            await bot.send_message(
                ORDERS_CHANNEL, f"Yangi buyurtma\n{data}\n\n#yangi_buyurtma"
            )
            await message.answer(
                "Buyurtmangiz qabul qilindi tez orada buyurtmangiz yetkaziladi",
                reply_markup=generate_menu_btns(),
            )


@dp.callback_query_handler(lambda callback_query: callback_query.data == "my_details")
async def give_an_order(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    client_order_history = get_client_order_details(user_id)
    user_details = get_user_details(chat_id=user_id)
    await callback_query.message.delete()
    await callback_query.message.answer(
        f"ℹ️ Sizning ma'lumotlaringiz: \n\n{user_details}\n\n{client_order_history}",
        reply_markup=back_to_main_menu_inline_btn,
    )


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == "exchange_bonus"
)
async def exchange_bonus(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_bonus = get_user_bonus(chat_id=user_id)
    await callback_query.message.delete()
    if user_bonus > 0:
        await callback_query.message.answer(
            f"Sizning bonuslaringiz soni: {user_bonus} ga teng.\n",
            reply_markup=bonus_btns,
        )
    else:
        await callback_query.message.answer(
            "Sizda bonus ballar mavjud emas, Bonus ballar yig'ish uchun aktiv mijozlarni jalb qiling ",
            reply_markup=generate_menu_btns(BONUS_MENU_BTNS),
        )


@dp.callback_query_handler(lambda callback_query: callback_query.data == "my_bonuses")
async def bonuses(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer(
        "Bonuslar menusi.",
        reply_markup=generate_menu_btns(btns=BONUS_MENU_BTNS),
    )


@dp.callback_query_handler(
    lambda callback_query: callback_query.data == "proceed_exchange_bonus"
)
async def proceed_exchange_bonus(callback_query: types.CallbackQuery):
    user_phone_num = get_user_phone_number(chat_id=callback_query.from_user.id)
    await callback_query.message.delete()
    await callback_query.message.answer(
        "Sizning so'rovingiz adminlarimizga yuborildi, tez orada so'rovingiz bo'yicha aloqaga chiqamiz.",
        reply_markup=generate_menu_btns(),
    )
    await bot.send_message(
        REGISTRATION_CHANNEL,
        f"Ushbu raqamdagi foydalanuvchi: {user_phone_num} \nbonus ballarini almashtirmoqchi\n#ball_ayirboshlash",
    )
