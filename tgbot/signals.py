import asyncio
from datetime import datetime
from django.db.models.signals import pre_delete, post_save, pre_save
from django.dispatch import receiver

from tgbot.bot.loader import bot
from tgbot.bot.keyboards import generate_order_btns, generate_menu_btns
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
    bonus = subscription.referal_bonus

    if user.referrer.exists():
        InOutCome.objects.create(
            status=1,
            account_id=user.payment_type,
            amount=subscription.cost,
            description=f"{user.full_name} {subscription.title} tarifiga to'lov qildi",  # noqa
        )
        referral = user.referrer.last()
        if referral.is_active:
            referrer_user = referral.referrer
            referrer_user.cashback += bonus
            referral.is_active = False

            referral.save()
            referrer_user.save()

            send_message(
                chat_id=referrer_user.chat_id,
                text="Tabriklaymiz, Siz taklif qilgan "
                f"{user.full_name} ning profili aktivlatshtirilda va sizga"
                f"{bonus} so'm bonus berildi va siz uning kelasi donalab sotib"
                f" oladigan xaridlaridan {subscription.cashback_amount} so'm "
                "cashback olasiz",
            )

    if user.bonus_in_percent < subscription.cashback_percent:
        user.bonus_in_percent = subscription.cashback_percent
        user.save()
        send_message(
            chat_id=user.chat_id,
            text=f"Tabriklaymiz 🥳, {subscription.title} tarifiga to'lov"
            " qilganingiz uchun siz keyingi har bir donalab sotib olgan"
            f"xaridingiz uchun {subscription.cashback_percent}% cashback"
            " olasiz",
        )
    if user.cashback_for_referer < subscription.cashback_amount:
        user.cashback_for_referer = subscription.cashback_amount
        user.save()


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
        number_of_products = instance.number_of_products
        product = instance.product
        customer = instance.customer
        cost_of_order = number_of_products * product.selling_price
        customer_payment_type = customer.payment_type

        if customer.subscription_based:
            subscription = customer.subscriptions.last()
            subscription.number_of_available_products -= number_of_products
            if not subscription.activation_date:
                subscription.activation_date = datetime.now()
            subscription.save()
        else:
            cashback_for_customer = (
                cost_of_order * customer.bonus_in_percent // 100
            )  # noqa
            customer.cashback += cashback_for_customer
            referrer = customer.referrer.first()
            send_message(
                customer.chat_id,
                f"Sizga {number_of_products} ta maxsulot harid qilganingiz uchun {cashback_for_customer:,} so'm bonus berildi",  # noqa
            )
            if referrer:
                referrer = referrer.referrer
                cashback_for_referer = (
                    number_of_products * customer.cashback_for_referer
                )
                referrer.cashback += cashback_for_referer
                referrer.save()
                send_message(
                    referrer.chat_id,
                    f"Tabriklaymiz, sizning taklif qilgan mijoz {customer.full_name}, {number_of_products} ta mahsulot sotib oldi va sizga {cashback_for_referer:,} so'm bonus berildi",  # noqa
                )

            InOutCome.objects.create(
                status=1,
                account_id=customer_payment_type,
                amount=cost_of_order,
                description=f"{customer.full_name} ga {number_of_products} ta mahsulot yetkazib berildi",  # noqa
            )

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
            asyncio.run(
                bot.send_message(
                    chat_id=instance.chat_id,
                    text="Tabriklaymiz, sizning profilingiz aktivlashtirildi",
                    reply_markup=generate_menu_btns(),
                )
            )


@receiver(pre_save, sender=UserSubscription)
def pre_save_user_subscription(sender, instance, **kwargs):
    user = instance.user
    subscription = instance.subscription

    if instance.pk:
        old_instance = sender.objects.get(pk=instance.pk)

        if old_instance.payment_status != 3 and instance.payment_status == 3:
            save_referal(user=user, subscription=subscription)

        if not old_instance.is_active and instance.is_active:
            save_referal(
                user=instance.user,
                subscription=instance.subscription,
            )

    elif not instance.pk and instance.payment_status == 3:
        save_referal(user=instance.user, subscription=instance.subscription)


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
