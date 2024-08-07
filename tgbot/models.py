from django.db import models
from django_lifecycle import (
    LifecycleModel,
    hook,
    BEFORE_UPDATE,
    BEFORE_DELETE,
    AFTER_CREATE,
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
    is_active = models.BooleanField(
        default=False,
        verbose_name="Aktivlik xolati",
    )
    subscription_based = models.BooleanField(
        default=True, verbose_name="Tarif bo'yicha sotib oladimi?"
    )
    role = models.IntegerField(
        choices=ROLE_CHOICES,
        default=2,
        verbose_name="Rol",
    )
    chat_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    state = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    full_name = models.CharField(
        max_length=250,
        default="",
        verbose_name="To'liq ism",
        blank=True,
    )
    phone_number = models.CharField(
        max_length=250, default="", verbose_name="Telefon raqam"
    )
    address = models.CharField(
        max_length=500,
        default="",
        verbose_name="Manzil",
    )
    cashback = models.BigIntegerField(
        default=0,
        verbose_name="cashback summasi",
    )
    bonus_in_percent = models.IntegerField(
        default=0, verbose_name="Donalab sotib olish uchun bonus foizi"
    )
    cashback_for_referer = models.IntegerField(default=0)
    payment_type = models.IntegerField(
        choices=PAYMENT_CHOICES, default=0, verbose_name="To'lov turi"
    )
    available_bottles = models.IntegerField(
        default=0, verbose_name="Bo'sh idishlar soni"
    )

    def __str__(self) -> str:
        return self.phone_number


class BonusExchange(models.Model):
    user = models.ForeignKey(
        TelegramUser, on_delete=models.CASCADE, verbose_name="Foydalanuvchi"
    )
    ball = models.IntegerField()
    comment = models.TextField(verbose_name="Izoh")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Yaratilgan vaqti"
    )
    updated_at = models.DateTimeField(auto_now=True)


class Curier(models.Model):
    full_name = models.CharField(
        max_length=255,
        null=True,
        verbose_name="To'liq ismi",
    )
    phone_number = models.CharField(
        max_length=20, null=True, verbose_name="Telefon raqami"
    )
    chat_id = models.CharField(
        max_length=255,
        null=True,
        verbose_name="Chat ID",
    )
    birth_date = models.DateField(null=True, verbose_name="Date of Birth")
    passport_data = models.CharField(
        max_length=255, null=True, verbose_name="Passport ma'lumotlari"
    )
    address = models.TextField(null=True, verbose_name="Manzil")
    phone_numbers_2 = models.CharField(
        max_length=255, null=True, verbose_name="2 chi telefon raqami"
    )
    car_model = models.CharField(
        max_length=255, null=True, verbose_name="Mashina modeli"
    )
    car_license_plate = models.CharField(
        max_length=255, null=True, verbose_name="Mashina davlat raqami"
    )

    def __str__(self):
        return f"{self.full_name} ({self.phone_number})"


class Referral(models.Model):
    referrer = models.ForeignKey(
        TelegramUser, on_delete=models.CASCADE, related_name="referrals"
    )
    referred_user = models.ForeignKey(
        TelegramUser, on_delete=models.CASCADE, related_name="referrer"
    )
    is_active = models.BooleanField(default=True)


class ProductTemplate(models.Model):
    title = models.CharField(verbose_name="Maxsulot nomi", max_length=250)
    volume_liters = models.IntegerField(verbose_name="Hajmi(Litrda): ")
    number_of_products = models.IntegerField()
    buying_price = models.IntegerField(verbose_name="Sotib olish narxi:")
    selling_price = models.IntegerField(verbose_name="Sotish narxi:")

    def __str__(self) -> str:
        return f"{self.title} - {self.volume_liters} Liters"


class Promotion(models.Model):
    number_of_stars = models.IntegerField(verbose_name="Bonus ballar")
    winning_price = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.number_of_stars} ⭐️ - {self.winning_price}"


class Subscription(models.Model):
    title = models.CharField(verbose_name="Tarif Nomi", max_length=255)
    product_template = models.ForeignKey(
        ProductTemplate, verbose_name="Maxsulot", on_delete=models.CASCADE
    )
    product_count = models.IntegerField(verbose_name="Maxsulot soni")
    cost = models.IntegerField(verbose_name="Sotilish narxi")
    cashback_percent = models.IntegerField(
        verbose_name="Keyingi xaridlari uchun cashback foizi"
    )
    referal_bonus = models.IntegerField(
        verbose_name="Referal bonusi (so'mda)", default=0
    )
    cashback_amount = models.IntegerField(
        verbose_name="Taklif qilgan foydalanuvchining har bir dona maxsulotdan olinadigan cashback summasi",  # noqa
        default=0,
    )
    expires_after = models.IntegerField(
        verbose_name="Necha kundan so'ng tarif passiv bo'ladi?"
    )

    class Meta:
        verbose_name = "Tarif"
        verbose_name_plural = "Tariflar"

    def __str__(self) -> str:
        return f"{self.title} - {self.product_count} - {self.cost}"


class UserSubscription(LifecycleModel):
    user = models.ForeignKey(
        TelegramUser, on_delete=models.CASCADE, related_name="subscriptions"
    )
    subscription = models.ForeignKey(
        Subscription, on_delete=models.CASCADE, verbose_name="Tarif"
    )
    activation_date = models.DateTimeField(null=True)
    number_of_available_products = models.IntegerField(default=0)
    payment_status = models.IntegerField(
        choices=PAYMENT_STATUS_CHOICES,
        default=1,
        verbose_name="To'lov statusi",
    )

    class Meta:
        verbose_name = "Foydalanuvchi Tarifi"
        verbose_name_plural = "Foydalanuvchi Tariflari"

    def __str__(self):
        return f"{self.user.full_name} - {self.subscription.title} - Activated on {self.activation_date}"  # noqa

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
    balance = models.IntegerField(verbose_name="Mavjud Summa")

    def __str__(self) -> str:
        return f"{self.get_type_display()}({self.name}) - {self.balance}"


class InOutCome(LifecycleModel):
    account = models.ForeignKey(
        Account,
        verbose_name="Xisob",
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField(verbose_name="Miqdor")
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Izoh",
    )
    date_added = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, choices=INOUTCOME_CHOICES)

    def __str__(self):
        return f"Income of {self.amount} for {self.account} added on {self.date_added}"  # noqa

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
    number_of_products = models.IntegerField(
        verbose_name="Sotib olingan maxsulot soni",
    )

    def __str__(self) -> str:
        if self.status == 1:
            return f"{self.product_template} - {self.product_template.buying_price} - {self.number_of_products}"  # noqa
        elif self.status == 2:
            return f"{self.product_template} - {self.product_template.selling_price} - {self.number_of_products}"  # noqa

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
                    self.product_template.buying_price * self.number_of_products  # noqa
                )
                self.product_template.number_of_products += (
                    self.number_of_products
                )  # noqa
            elif self.status == 2:
                self.account.balance += (
                    self.product_template.selling_price
                    * self.number_of_products  # noqa
                )
                self.product_template.number_of_products -= (
                    self.number_of_products
                )  # noqa

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
        TelegramUser,
        on_delete=models.CASCADE,
        verbose_name="Klient",
        related_name="orders",
    )
    number_of_products = models.IntegerField(
        verbose_name="Buyurtma qilingan maxsulotlar"
    )
    curier = models.ForeignKey(
        Curier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_orders",
        verbose_name="Kurier",
    )
    product = models.ForeignKey(
        ProductTemplate,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Maxsulot",
    )
    status = models.IntegerField(choices=ORDER_STATUS_CHOICES, default=1)
    created_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Buyurtma berilgan vaqti"
    )
    finished_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Buyurtma tugatilgan vaqti",
    )
    updated_at = models.DateTimeField(auto_now=True)
