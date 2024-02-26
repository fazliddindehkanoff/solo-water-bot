from tgbot.models import Order, TelegramUser, Subscription, Referral


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
        subscription_detail = f"📜 Tarif nomi: {subscription.title} \n🫙 Kapsulalar soni: {subscription.product_count}\n🧮 Bonus ball:{subscription.bonus}\n💰 Tarif narxi: {subscription.cost}\n"

    return subscription_detail


def get_cliend_data(user_id: str) -> str:
    client_data = ""
    user = TelegramUser.objects.filter(chat_id=user_id).first()
    if user:
        client_data = f"\n<b>ID</b>: {user.pk}\n<b>Mijoz ismi:</b> {user.full_name}\n<b>Tanlangan ta'rif:</b> {user.subscriptions.first().subscription.title}\n<b>To'lov turi:</b> {user.get_payment_type_display()}\n<b>Manzil:</b> {user.address}\n<b>Telefon raqami:</b> {user.phone_number}"

    return client_data


def generate_referal_link(user_id: str) -> str:
    return f"https://t.me/farqiyoooobot?start={user_id}"


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


def get_client_order_details(user_id: str):
    data = ""
    user = TelegramUser.objects.filter(chat_id=user_id).first()
    orders = Order.objects.filter(customer=user)
    for order in orders:
        data += get_order_details(order) + "\n"

    if not data:
        data = "Siz hali hech qanday buyurtma bermagansiz"
    return data


def get_order_details(order):
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


def get_user_bonuses():
    data = "<b>Foydalanuvchilar yig'gan ballari:</b>\n\n"
    users = TelegramUser.objects.filter(role=2).order_by("-bonus_balance")
    for index, user in enumerate(users, start=1):
        data += f"{index}. {user.full_name}({user.bonus_balance})\n"

    return data
