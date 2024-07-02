import asyncio
from datetime import datetime
from django.db.models.signals import pre_delete, post_save, pre_save
from django.dispatch import receiver

from tgbot.bot.loader import bot
from tgbot.bot.keyboards import generate_order_btns
from tgbot.utils import send_message
from .models import (
    BonusExchange,
    InOutCome,
    Order,
    ProductInOut,
    TelegramUser,
    UserSubscription,
)


def save_referal(user, subscription):
    bonus = subscription.bonus
    cashback_amount = subscription.cashback_amount

    if user.referrer.exists():
        referral = user.referrer.last()
        if referral.is_active:
            referrer_user = referral.referrer
            referrer_user.bonus_balance += bonus
            referral.is_active = False

            referral.save()
            referrer_user.save()

            send_message(
                chat_id=referrer_user.chat_id,
                text="Tabriklaymiz, Siz taklif qilgan "
                f"{user.full_name} "
                f"ning profili aktivlatshtirilda va sizga {bonus} "
                "ball bonus berildi",
            )

    user.cashback += cashback_amount
    user.save()
    send_message(
        chat_id=user.chat_id,
        text=f"Tabriklaymiz 🥳, {subscription.title} tarifiga to'lov"
        f" qilganingiz uchun sizga {cashback_amount} so'm kashbak"
        " taqdim etildi",
    )


@receiver(pre_delete, sender=ProductInOut)
def pre_delete_product_income(sender, instance, **kwargs):
    instance.before_delete_decrease_number_of_products()


@receiver(post_save, sender=Order)
def send_courier_assignment_notification(sender, instance, created, **kwargs):
    if instance.curier and instance.status == 1:
        asyncio.run(
            send_notification_async(
                instance.curier.chat_id,
                instance.id,
                instance.number_of_products,
                instance.customer.address,
            )
        )
    if instance.status == 2 and not instance.finished_date:
        instance.customer.available_bottles += instance.number_of_products
        instance.finished_date = datetime.now()

        customer = instance.customer
        customer_payment_type = customer.payment_type
        subscription = customer.subscriptions.last()
        number_of_products = instance.number_of_products
        product = instance.product

        if subscription:
            subscription.number_of_available_products -= number_of_products
            if not subscription.activation_date:
                subscription.activation_date = datetime.now()
            subscription.save()

        if customer_payment_type == 1:
            account_id = 2

        elif customer_payment_type == 2:
            account_id = 1

        ProductInOut.objects.create(
            status=2,
            account_id=account_id,
            product_template=product,
            number_of_products=number_of_products,
        )
        InOutCome.objects.create(
            status=1,
            account_id=customer_payment_type,
            amount=number_of_products * product.selling_price,  # noqa
            description=f"{customer.full_name} ga {number_of_products} ta mahsulot yetkazib berildi",  # noqa
        )

        customer.save()
        instance.save()


async def send_notification_async(chat_id, order_id, num_products, address):
    message = "Assalomu alaykum, sizga yangi buyurtma yuklatildi:\n"
    f"Buyurtma raqami: {order_id}\nKapsulalar soni: {num_products}\nManzil: "
    f"{address}\n\nUshbu buyurtmani qabul qilasizmi?"
    await bot.send_message(
        chat_id=chat_id,
        text=message,
        reply_markup=generate_order_btns(order_id=order_id),
    )


@receiver(pre_save, sender=TelegramUser)
def before_save_telegram_user(sender, instance, **kwargs):
    if instance.pk:
        old_instance = sender.objects.get(pk=instance.pk)
        if not old_instance.is_active and instance.is_active:
            send_message(
                chat_id=instance.chat_id,
                text="Tabriklaymiz, sizning profilingiz aktivlashtirildi",
            )


@receiver(post_save, sender=UserSubscription)
def create_income_and_add_bonus(sender, instance, created, **kwargs):
    user = instance.user
    subscription = instance.subscription

    InOutCome.objects.create(
        status=1,
        account_id=user.payment_type,
        amount=subscription.cost,
        description=f"{user.full_name} {subscription.title} tarifiga to'lov qildi",  # noqa
    )

    if created:
        if instance.payment_status == 3:
            save_referal(user=user, subscription=subscription)

    else:
        old_instance = sender.objects.get(pk=instance.pk)
        print(old_instance.payment_status != 3 and instance.payment_status == 3)
        if old_instance.payment_status != 3 and instance.payment_status == 3:
            save_referal(user=user, subscription=subscription)


@receiver(post_save, sender=BonusExchange)
def decrease_user_bonus(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        ball = instance.ball
        if user.bonus_balance < ball:
            instance.error_flag = True
            instance.save()
        else:
            instance.error_flag = False
            user.bonus_balance -= ball
            instance.save()
            user.save()
