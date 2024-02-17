from django.db import models

from .constants import ROLE_CHOICES


class TelegramUser(models.Model):
    chat_id = models.CharField(max_length=255)
    role = models.IntegerField(choices=ROLE_CHOICES, default=3)


class ProductTemplate(models.Model):
    title = models.CharField(max_length=250)
    litr = models.IntegerField()
    number_of_products = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.title} - {self.litr} Litr"


class ProductIncome(models.Model):
    product = models.ForeignKey(ProductTemplate, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_products = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.product} - {self.price} - {self.number_of_products}"


class ProductOutcome(models.Model):
    product = models.ForeignKey(ProductTemplate, on_delete=models.CASCADE)
    sold_price = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_products = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.product} - {self.selling_price} - {self.number_of_products}"


class Promotion(models.Model):
    number_of_stars = models.IntegerField()
    winning_price = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.number_of_stars} ⭐️ - {self.winning_price}"


class Subscription(models.Model):
    title = models.CharField(max_length=255)
    product = models.ForeignKey(ProductTemplate, on_delete=models.CASCADE)
    product_count = models.IntegerField()
    bonus = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.title} - {self.product_count} - {self.cost}"


class Income(models.Model):
    pass


class Outcome(models.Model):
    pass
