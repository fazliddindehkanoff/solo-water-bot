from aiogram import types
from tgbot.bot.loader import bot

from .models import Curier, Order, Referral, TelegramUser, UserSubscription


def register_user(user_id: str, user_role: int = 2) -> tuple[int, bool]:
    user = TelegramUser.objects.filter(chat_id=user_id).first()
    if not user:
        if user_role == 3:
            Curier.objects.create(chat_id=user_id)
        TelegramUser.objects.create(chat_id=user_id, role=user_role)
        return user_role, False
    else:
        return user.role, True


def set_state(user_id: str, state: str):
    user = TelegramUser.objects.filter(chat_id=user_id).first()
    if user:
        user.state = state
        user.save()


def set_user_data(user_id: str, field: str, value: str):
    user = TelegramUser.objects.filter(chat_id=user_id).first()
    if hasattr(user, field):
        setattr(user, field, value)
        user.save()
    if field == "subscription":
        UserSubscription.objects.create(user=user, subscription_id=value)


def set_courier_data(chat_id: str, field: str, value: str):
    user = Curier.objects.filter(chat_id=chat_id).first()
    if hasattr(user, field):
        setattr(user, field, value)
        user.save()


def create_referal(user_id, refered_user_id):
    referrer = TelegramUser.objects.filter(chat_id=refered_user_id).first()
    referred_user = TelegramUser.objects.filter(chat_id=user_id).first()
    if referrer and referred_user:
        Referral.objects.create(referrer=referrer, referred_user=referred_user)


def create_order(user_id: str, number_of_products: int) -> int:
    order_id = 0
    user = TelegramUser.objects.filter(chat_id=user_id).first()
    subscription = user.subscriptions.last()
    if user and user.subscriptions.last():
        try:
            order = Order.objects.create(
                customer=user,
                number_of_products=number_of_products,
                product=subscription.subscription.product_template,
            )
            order_id = order.pk
        except Exception as e:
            print(e)

    return order_id


async def forward_post_to_all_users(message: types.Message):
    # Retrieve all users from the database
    all_users = TelegramUser.objects.filter(role=2).all()
    post_content = message.text
    media_file = None

    if message.photo:
        media_file = message.photo[-1].file_id
        post_content = message.caption
    elif message.video:
        media_file = message.video.file_id
        post_content = message.caption

    # Forward the post to each user
    for user in all_users:
        try:
            if media_file:
                # Send the media file along with the text content
                await bot.send_photo(user.chat_id, media_file, caption=post_content)
            else:
                await bot.send_message(user.chat_id, post_content)
        except Exception as e:
            print(f"Failed to send post to user {user.chat_id}: {str(e)}")


def remove_kurier_from_order(order_id):
    try:
        order = Order.objects.get(id=order_id)
        order.curier = None
        order.save()
    except Order.DoesNotExist:
        pass


def update_order_status(order_id: int, status: int):
    try:
        order = Order.objects.get(id=order_id)
        order.status = status
        order.save()
    except Order.DoesNotExist:
        pass
