from django.db import models
from django.utils import timezone
from django_lifecycle import (
    LifecycleModel,
    hook,
    BEFORE_UPDATE,
    BEFORE_DELETE,
    AFTER_CREATE,
    AFTER_UPDATE,
)

from .constants import (
    ACCOUNT_TYPE_CHOICES,
    INOUTCOME_CHOICES,
    ORDER_STATUS_CHOICES,
    PAYMENT_CHOICES,
    PAYMENT_STATUS_CHOICES,
    ROLE_CHOICES,
    SALES_CHOICES,
)


class TelegramUser(LifecycleModel):
    is_active = models.BooleanField(default=False, verbose_name="Aktivlik xolati")
    payment_status = models.IntegerField(
        choices=PAYMENT_STATUS_CHOICES, default=1, verbose_name="To'lov statusi"
    )
    role = models.IntegerField(choices=ROLE_CHOICES, default=2, verbose_name="Rol")
    chat_id = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    full_name = models.CharField(max_length=250, default="", verbose_name="To'liq ism")
    phone_number = models.CharField(
        max_length=250, default="", verbose_name="Telefon raqam"
    )
    address = models.CharField(max_length=500, default="", verbose_name="Manzil")
    bonus_balance = models.IntegerField(default=0, verbose_name="Bonus ballar")
    payment_type = models.IntegerField(
        choices=PAYMENT_CHOICES, default=0, verbose_name="To'lov turi"
    )

    def __str__(self) -> str:
        return self.full_name

    @hook(AFTER_UPDATE, when="is_active")
    def add_bonus(self):
        if (
            self.referrer.exists() and self.is_active
        ):  # Check if there are any referrals
            referral = self.referrer.first()  # Get the first related Referral object
            referrer_user = referral.referrer  # Get the related TelegramUser object
            bonus = self.subscriptions.last().subscription.bonus
            referrer_user.bonus_balance += bonus
            referrer_user.save()


class Curier(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="To'liq ismi")
    phone_number = models.CharField(max_length=20, verbose_name="Telefon raqami")
    chat_id = models.CharField(max_length=255, verbose_name="Chat ID")
    birth_date = models.DateField(verbose_name="Date of Birth")
    passport_data = models.CharField(
        max_length=255, verbose_name="Passport ma'lumotlari"
    )
    address = models.TextField(verbose_name="Manzil")
    phone_numbers_2 = models.CharField(
        max_length=255, verbose_name="2 chi telefon raqami"
    )
    car_model = models.CharField(max_length=255, verbose_name="Mashina modeli")
    car_license_plate = models.CharField(
        max_length=255, verbose_name="Mashina davlat raqami"
    )

    def __str__(self):
        return self.full_name


class Referral(models.Model):
    referrer = models.ForeignKey(
        TelegramUser, on_delete=models.CASCADE, related_name="referrals"
    )
    referred_user = models.ForeignKey(
        TelegramUser, on_delete=models.CASCADE, related_name="referrer"
    )


class ProductTemplate(models.Model):
    title = models.CharField(verbose_name="Maxsulot nomi", max_length=250)
    volume_liters = models.IntegerField(verbose_name="Hajmi(Litrda): ")
    number_of_products = models.IntegerField()
    buying_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Sotib olish narxi:"
    )
    selling_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Sotish narxi:"
    )

    def __str__(self) -> str:
        return f"{self.title} - {self.volume_liters} Liters"


class Promotion(models.Model):
    number_of_stars = models.IntegerField()
    winning_price = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.number_of_stars} ⭐️ - {self.winning_price}"


class Subscription(models.Model):
    title = models.CharField(verbose_name="Tarif Nomi", max_length=255)
    product_template = models.ForeignKey(
        ProductTemplate, verbose_name="Maxsulot", on_delete=models.CASCADE
    )
    product_count = models.IntegerField(verbose_name="Maxsulot soni")
    bonus = models.IntegerField(verbose_name="Qo'shiladigan bonus bali")
    cost = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Sotilish narxi"
    )
    expires_after = models.IntegerField(
        verbose_name="Necha kundan so'ng tarif passiv bo'ladi?"
    )

    def __str__(self) -> str:
        return f"{self.title} - {self.product_count} - {self.cost}"


class UserSubscription(LifecycleModel):
    user = models.ForeignKey(
        TelegramUser, on_delete=models.CASCADE, related_name="subscriptions"
    )
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    activation_date = models.DateTimeField(null=True)
    number_of_available_products = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.full_name} - {self.subscription.title} - Activated on {self.activation_date}"

    @property
    def is_active(self):
        return (
            self.activation_date
            and self.number_of_available_products > 0
            and self.user.is_active
        )

    @hook(AFTER_CREATE)
    def set_number_of_available_products(self):
        self.number_of_available_products = self.subscription.product_count
        self.save()


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


class InOutCome(LifecycleModel):
    account = models.ForeignKey(Account, verbose_name="Xisob", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Miqdor")
    description = models.TextField(blank=True, null=True, verbose_name="Izoh")
    date_added = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=INOUTCOME_CHOICES, verbose_name="Status")

    def __str__(self):
        return f"Income of {self.amount} for {self.account} added on {self.date_added}"

    @hook(AFTER_CREATE)
    def update_account(self):
        if self.status == 1:
            self.account.balance += self.amount
        else:
            self.account.balance -= self.amount
        self.account.save()

    @hook(BEFORE_DELETE)
    def before_delete(self):
        if self.status == 1:
            self.account.balance -= self.amount
        else:
            self.account.balance += self.amount
        self.account.save()


class ProductInOut(LifecycleModel):
    status = models.IntegerField(choices=SALES_CHOICES, default=1)
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, verbose_name="Account"
    )
    product_template = models.ForeignKey(
        ProductTemplate, on_delete=models.CASCADE, verbose_name="Maxsulot nomi"
    )
    number_of_products = models.IntegerField(verbose_name="Sotib olingan maxsulot soni")

    def __str__(self) -> str:
        if self.status == 1:
            return f"{self.product_template} - {self.product_template.buying_price} - {self.number_of_products}"
        elif self.status == 2:
            return f"{self.product_template} - {self.product_template.selling_price} - {self.number_of_products}"

    @hook(AFTER_CREATE)
    def after_create_increase_number_of_products(self):
        if self.status == 1:
            self.account.balance -= (
                self.product_template.buying_price * self.number_of_products
            )
            self.product_template.number_of_products += self.number_of_products
        elif self.status == 2:
            self.account.balance += (
                self.product_template.selling_price * self.number_of_products
            )
            self.product_template.number_of_products -= self.number_of_products
        self.account.save()
        self.product_template.save()

    @hook(BEFORE_UPDATE)
    def before_update_increase_number_of_products(self):
        original_instance = ProductInOut.objects.get(pk=self.pk)
        if original_instance.status != self.status:
            if original_instance.status == 1:
                self.account.balance += (
                    original_instance.product_template.buying_price
                    * original_instance.number_of_products
                )
                self.product_template.number_of_products -= (
                    original_instance.number_of_products
                )
            elif original_instance.status == 2:
                self.account.balance -= (
                    original_instance.product_template.selling_price
                    * original_instance.number_of_products
                )
                self.product_template.number_of_products += (
                    original_instance.number_of_products
                )
            if self.status == 1:
                self.account.balance -= (
                    self.product_template.buying_price * self.number_of_products
                )
                self.product_template.number_of_products += self.number_of_products
            elif self.status == 2:
                self.account.balance += (
                    self.product_template.selling_price * self.number_of_products
                )
                self.product_template.number_of_products -= self.number_of_products

            self.account.save()
            self.product_template.save()

    @hook(BEFORE_DELETE)
    def before_delete_decrease_number_of_products(self):
        if self.status == 1:
            self.product_template.number_of_products -= self.number_of_products
            self.account.balance += (
                self.product_template.buying_price * self.number_of_products
            )
        elif self.status == 2:
            self.product_template.number_of_products += self.number_of_products
            self.account.balance -= (
                self.product_template.selling_price * self.number_of_products
            )

        self.product_template.save()
        self.account.save()


class Order(LifecycleModel):
    customer = models.ForeignKey(
        TelegramUser, on_delete=models.CASCADE, verbose_name="Klient"
    )
    number_of_products = models.IntegerField(
        verbose_name="Buyurtma qilingan maxsulotlar"
    )
    curier = models.ForeignKey(
        TelegramUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name="related_orders",
        verbose_name="Kurier",
    )
    product = models.ForeignKey(ProductTemplate, on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(choices=ORDER_STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Yaratilgan vaqti"
    )
    updated_at = models.DateTimeField(auto_now=True)

    @hook(AFTER_CREATE)
    def set_subscription_activated_date(self):
        subscription = self.customer.subscriptions.last()
        if subscription:
            subscription.number_of_available_products -= self.number_of_products
            if not subscription.activation_date:
                subscription.activation_date = timezone.now()
            subscription.save()
        else:
            print("No subscription found for the customer:", self.customer)

    @hook(AFTER_UPDATE)
    def create_product_out(self):
        if self.status == 2:
            if self.customer.payment_type == 1:
                account_id = 2
            elif self.customer.payment_type == 2:
                account_id = 1
            ProductInOut.objects.create(
                status=2,
                account_id=account_id,
                product_template=self.product,
                number_of_products=self.number_of_products,
            )
