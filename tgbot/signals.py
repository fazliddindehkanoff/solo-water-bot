import asyncio
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

from tgbot.bot.loader import bot
from tgbot.bot.keyboards import generate_order_btns
from .models import Order, ProductInOut


@receiver(pre_delete, sender=ProductInOut)
def pre_delete_product_income(sender, instance, **kwargs):
    """
    Signal handler to decrement the number of products associated with ProductIncome
    instances when they are deleted.
    """
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


async def send_notification_async(chat_id, order_id, num_products, address):
    message = f"Assalomu alaykum, sizga yangi buyurtma yuklatildi:\nBuyurtma raqami: {order_id}\nKapsulalar soni: {num_products}\nManzil: {address}\n\nUshbu buyurtmani qabul qilasizmi?"
    await bot.send_message(
        chat_id=chat_id,
        text=message,
        reply_markup=generate_order_btns(order_id=order_id),
    )
