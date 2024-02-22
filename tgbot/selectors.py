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
