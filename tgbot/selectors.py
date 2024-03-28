from tgbot.models import Curier, Order, TelegramUser, Subscription


def get_state(user_id: str) -> str:
    user = TelegramUser.objects.filter(chat_id=user_id).first()
    if user:
        return user.state
    return ""


def get_subscriptions_info() -> tuple[str, list[int]]:
    subscriptions_details = ""
    subscriptions_ids = []
    subscriptions = Subscription.objects.all()
    for index, subscription in enumerate(subscriptions, start=1):
        subscriptions_ids.append(subscription.pk)
        subscriptions_details += (
            f"{index}) {get_subscription_detail(subscription.pk)}\n"
        )

    return subscriptions_details, subscriptions_ids


def get_subscription_detail(subscription_id: int) -> str:
    subscription_detail = ""
    subscription = Subscription.objects.filter(id=subscription_id).first()

    if subscription:
        subscription_detail = f"📜 Tarif nomi: {subscription.title} \n🫙 Kapsulalar soni: {subscription.product_count}\n🧮 Bonus ball:{subscription.bonus}\n💰 Tarif narxi: {subscription.cost:,} so'm\n"

    return subscription_detail


def get_cliend_data(user_id: str) -> str:
    client_data = ""
    user = TelegramUser.objects.filter(chat_id=user_id).first()
    if user:
        client_data = f"\n<b>ID</b>: {user.pk}\n<b>Mijoz ismi:</b> {user.full_name}\n<b>Tanlangan ta'rif:</b> {user.subscriptions.first().subscription.title}\n<b>To'lov turi:</b> {user.get_payment_type_display()}\n<b>Manzil:</b> {user.address}\n<b>Telefon raqami:</b> {user.phone_number}"

    return client_data


def generate_referal_link(user_id: str) -> str:
    return f"https://t.me/SoloWaterBot?start={user_id}"


def get_referralers_data(user_id: str) -> str:
    data = ""
    user = TelegramUser.objects.filter(chat_id=user_id).first()
    if user:
        for index, referraler in enumerate(user.referrals.all(), start=1):
            data += f"{index}. {referraler.referred_user.full_name} - {referraler.referred_user.bonus_balance}"

    return data


def is_user_active(user_id: str) -> bool:
    user = TelegramUser.objects.filter(chat_id=user_id).first()
    return user and user.is_active


def get_number_of_available_products(user_id: str) -> int:
    user = TelegramUser.objects.filter(chat_id=user_id).first()
    if user:
        return user.subscriptions.last().number_of_available_products
    return 0


def get_cliend_order_data(user_id: str, order_id: int, number_of_products: int) -> str:
    client_data = ""
    order = Order.objects.filter(pk=order_id).first()
    user = TelegramUser.objects.filter(chat_id=user_id).first()
    if user and order:
        client_data = f"<b>Buyurtma raqami</b>: #{order.pk}\n<b>Mijoz ismi:</b> {user.full_name}\n<b>Maxsulot soni:</b> {number_of_products}\n<b>Manzil:</b> {user.address}\n<b>Telefon raqami:</b> {user.phone_number}"

    return client_data


def get_client_order_details(user_id: str) -> str:
    data = ""
    user = TelegramUser.objects.filter(chat_id=user_id).first()
    orders = Order.objects.filter(customer=user)
    for order in orders:
        data += get_order_details(order) + "\n"

    if not data:
        data = "Siz hali hech qanday buyurtma bermagansiz"
    return data


def get_order_details(order) -> str:
    data = ""
    if order:
        created_at_formatted = order.created_at.strftime("%Y-%m-%d %H:%M:%S")
        data = f"<b>Buyurtma raqami: </b>{order.id}\n<b>Buyurtma xolati: </b> {order.get_status_display()}\n<b>Buyurtma berilgan vaqt: </b> {created_at_formatted}\n<b>Maxsulot soni: </b> {order.number_of_products}\n"
    return data


def get_stats() -> str:
    orders = Order.objects.all()
    number_of_ordered_products = 0

    for order in orders:
        number_of_ordered_products += order.number_of_products

    tg_users = TelegramUser.objects.all()

    result = f"<b>Bot statistikasi:</b>\n\n<b>Umumiy buyurmalar soni:</b> {orders.count()}\n<b>Buyurtma qilingan suvlar soni:</b> {number_of_ordered_products}\n<b>Kurierlar soni:</b> {tg_users.filter(role=3).count()}\n<b>Foydalanuvchilar soni: {tg_users.filter(role=2).count()}</b>"

    return result


def get_user_bonuses() -> str:
    data = "<b>Foydalanuvchilar yig'gan ballari:</b>\n\n"
    users = TelegramUser.objects.filter(role=2).order_by("-bonus_balance")
    for index, user in enumerate(users, start=1):
        data += f"{index}. {user.full_name}({user.bonus_balance})\n"

    return data


def get_user_bonus(chat_id: str) -> int:
    user = TelegramUser.objects.filter(chat_id=chat_id).first()

    if user:
        return user.bonus_balance


def get_user_phone_number(chat_id: str) -> str:
    phone_number = ""
    user = TelegramUser.objects.filter(chat_id=chat_id).first()

    if user:
        phone_number = user.phone_number

    return phone_number


def get_user_details(chat_id: str) -> str:
    data = ""
    user = TelegramUser.objects.filter(chat_id=chat_id).first()

    if user:
        orders_count = user.orders.count()
        _last_sub = user.subscriptions.last().subscription
        subscription_title = _last_sub.title
        maximum_products = _last_sub.product_count
        ordered_products_count = 0
        for order in user.orders.all():
            ordered_products_count += order.number_of_products
        data = f"🧮 <b>Buyurtmalar soni: </b>{orders_count}\n💧 <b>Buyurtma qilingan suvlar: </b>{ordered_products_count}\n📋 <b>Hozirgi ta'rif nomi: </b>{subscription_title}\n🫙 <b>Tarif bo'yicha kapsulalar soni: </b> {maximum_products}"

    return data


def get_courier_details_formatted(user_id):
    try:
        courier = Curier.objects.get(chat_id=user_id)
        taken_orders_count = courier.assigned_orders.count()
        finished_orders = courier.assigned_orders.filter(status=2)
        car_model = courier.car_model
        car_license_plate = courier.car_license_plate
        delivered_products_count = 0

        for order in finished_orders:
            delivered_products_count += order.number_of_products

        formatted_details = (
            f"🚚 <b>Yuklangan buyurtmalar soni:</b> {taken_orders_count}\n"
            f"📦 <b>Bajarilgan buyurtmalar soni:</b> {finished_orders.count()}\n"
            f"📦 <b>Yetkazilgan mahsulotlar soni:</b> {delivered_products_count}\n"
            f"🚗 <b>Mashina modeli:</b> {car_model}\n"
            f"🚗 <b>Mashina davlat raqami:</b> {car_license_plate}\n"
        )

        return formatted_details

    except Curier.DoesNotExist:
        return "Kuryer ma'lumotlari topilmadi."


def get_finished_orders_details(user_id):
    try:
        courier = Curier.objects.get(chat_id=user_id)
        finished_orders = courier.assigned_orders.filter(status=2)

        if finished_orders.exists():
            formatted_orders = ""
            for order in finished_orders:
                formatted_created_at = order.created_at.strftime("%H:%M:%S %d.%m.%Y")
                formatted_order = (
                    f"<b>Buyurtma raqami:</b> #{order.id}\n"
                    f"<b>Buyurtma xolati:</b> Tugallandi\n"
                    f"<b>Buyurtma berilgan vaqt:</b> {formatted_created_at}\n"
                    f"<b>Maxsulot soni:</b> {order.number_of_products}\n\n"
                )
                formatted_orders += formatted_order

            return formatted_orders
        else:
            return "Tugallangan buyurtmalar topilmadi."

    except Curier.DoesNotExist:
        return "Kuryer ma'lumotlari topilmadi."


def get_curier_data(chat_id: str) -> str:
    try:
        curier = Curier.objects.get(chat_id=chat_id)
        formatted_data = (
            f"<b>To'liq ism:</b> {curier.full_name}\n"
            f"<b>Birinchi telefon raqami:</b> {curier.phone_number}\n"
            f"<b>Ikkinchi telefon raqami:</b> {curier.phone_numbers_2}\n"
            f"<b>Mashina modeli:</b> {curier.car_model}\n"
            f"<b>Mashina davlat raqami:</b> {curier.car_license_plate}"
        )
        return formatted_data
    except Curier.DoesNotExist:
        return "Kuryer ma'lumotlari topilmadi."


def get_order_notification_text(order_id):
    try:
        order = Order.objects.get(id=order_id)
        customer_name = order.customer.full_name
        product_name = order.product.title
        number_of_products = order.number_of_products

        # Formatted text in Uzbek
        text = f"Assalomu alaykum, {customer_name}!\n\n"
        text += f"Sizning buyurtmangiz yetkazib berilmoqda:\n"
        text += f"Maxsulot: {product_name}\n"
        text += f"Soni: {number_of_products}\n"
        text += "Holati: Yetkazib berilmoqda\n"

        # Get customer's chat ID
        chat_id = order.customer.chat_id

        return text, chat_id
    except Order.DoesNotExist:
        return None, None


def get_client_chat_id(order_id: int) -> str:
    try:
        order = Order.objects.get(id=order_id)
        return order.customer.chat_id
    except Order.DoesNotExist:
        return ""
