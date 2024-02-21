from django.db import models
from django_lifecycle import (
    LifecycleModel,
    hook,
    BEFORE_UPDATE,
    BEFORE_DELETE,
    AFTER_CREATE,
)

from .constants import ACCOUNT_TYPE_CHOICES, ROLE_CHOICES


class TelegramUser(models.Model):
    chat_id = models.CharField(max_length=255)
    role = models.IntegerField(choices=ROLE_CHOICES, default=3)
    state = models.CharField(max_length=255)
    full_name = models.CharField(max_length=250, default="")
    phone_number = models.CharField(max_length=250, default="")
    longitude = models.CharField(max_length=250, default="")
    latitude = models.CharField(max_length=250, default="")


class ProductTemplate(models.Model):
    title = models.CharField(verbose_name="Maxsulot nomi", max_length=250)
    volume_liters = models.IntegerField(verbose_name="Hajmi(Litrda): ")
    number_of_products = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.title} - {self.volume_liters} Liters"


class Promotion(models.Model):
    number_of_stars = models.IntegerField()
    winning_price = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.number_of_stars} ⭐️ - {self.winning_price}"


class Subscription(models.Model):
    title = models.CharField(max_length=255)
    product_template = models.ForeignKey(ProductTemplate, on_delete=models.CASCADE)
    product_count = models.IntegerField()
    bonus = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.title} - {self.product_count} - {self.cost}"


class Account(models.Model):
    name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Xisob raqam"
    )
    type = models.IntegerField(
        choices=ACCOUNT_TYPE_CHOICES, verbose_name="Xisob raqam turi"
    )
    balance = models.DecimalField(
        max_digits=20, decimal_places=2, verbose_name="Mavjud Summa"
    )

    def __str__(self) -> str:
        return f"{self.get_type_display()}({self.name}) - {self.balance}"


class Income(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Income of {self.amount} for {self.account} added on {self.date_added}"


class Outcome(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Outcome of {self.amount} for {self.account} added on {self.date_added}"


class ProductOutcome(LifecycleModel):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, verbose_name="Account"
    )
    product_template = models.ForeignKey(
        ProductTemplate, on_delete=models.CASCADE, verbose_name="Product Name"
    )
    sold_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Sold Price"
    )
    number_of_products = models.IntegerField(verbose_name="Number of Products")

    def __str__(self) -> str:
        return (
            f"{self.product_template} - {self.sold_price} - {self.number_of_products}"
        )

    @hook(AFTER_CREATE)
    def after_create_decrease_number_of_products(self):
        self.account.balance += self.sold_price * self.number_of_products
        self.product_template.number_of_products -= self.number_of_products
        self.account.save()
        self.product_template.save()

    @hook(BEFORE_UPDATE)
    def before_update_decrease_number_of_products(self):
        original_instance = ProductOutcome.objects.get(pk=self.pk)
        self.product_template.number_of_products -= (
            self.number_of_products - original_instance.number_of_products
        )
        self.account.balance -= (
            original_instance.sold_price * original_instance.number_of_products
        )
        self.account.balance += self.sold_price * self.number_of_products
        self.account.save()
        self.product_template.save()

    @hook(BEFORE_DELETE)
    def before_delete_increase_number_of_products(self):
        self.product_template.number_of_products += self.number_of_products
        self.product_template.save()

        self.account.balance -= self.sold_price * self.number_of_products
        self.account.save()


class ProductIncome(LifecycleModel):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, verbose_name="Account"
    )
    product_template = models.ForeignKey(
        ProductTemplate, on_delete=models.CASCADE, verbose_name="Maxsulot nomi"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Maxsulotning sotib olingan narxi"
    )
    number_of_products = models.IntegerField(verbose_name="Sotib olingan maxsulot soni")

    def __str__(self) -> str:
        return f"{self.product_template} - {self.price} - {self.number_of_products}"

    @hook(AFTER_CREATE)
    def after_create_increase_number_of_products(self):
        self.account.balance -= self.price * self.number_of_products
        self.product_template.number_of_products += self.number_of_products
        self.account.save()
        self.product_template.save()

    @hook(BEFORE_UPDATE)
    def before_update_increase_number_of_products(self):
        original_instance = ProductOutcome.objects.get(pk=self.pk)
        self.product_template.number_of_products += (
            self.number_of_products - original_instance.number_of_products
        )
        self.account.balance += (
            original_instance.price * original_instance.number_of_products
        )
        self.account.balance -= self.price * self.number_of_products
        self.account.save()
        self.product_template.save()

    @hook(BEFORE_DELETE)
    def before_delete_decrease_number_of_products(self):
        self.product_template.number_of_products -= self.number_of_products
        self.product_template.save()

        self.account.balance += self.price * self.number_of_products
        self.account.save()
