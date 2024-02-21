from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import ProductInOut


@receiver(pre_delete, sender=ProductInOut)
def pre_delete_product_income(sender, instance, **kwargs):
    """
    Signal handler to decrement the number of products associated with ProductIncome
    instances when they are deleted.
    """
    instance.before_delete_decrease_number_of_products()
