from django.contrib import admin

from .models import (
    TelegramUser,
    ProductIncome,
    ProductTemplate,
    ProductOutcome,
    Promotion,
    Subscription,
    Account,
    Income,
    Outcome,
)

from django.contrib import admin
from unfold.admin import ModelAdmin


@admin.register(Account)
class AccountAdminClass(ModelAdmin):
    list_display = ["type", "name", "balance"]


@admin.register(Income)
class IncomeAdminClass(ModelAdmin):
    pass


@admin.register(Outcome)
class OutcomeAdminClass(ModelAdmin):
    pass


@admin.register(Promotion)
class PromotionAdminClass(ModelAdmin):
    list_display = ["number_of_stars", "winning_price"]


@admin.register(Subscription)
class SubscriptionAdminClass(ModelAdmin):
    list_display = ["title", "cost", "product_count", "bonus"]


@admin.register(TelegramUser)
class TelegramUserAdminClass(ModelAdmin):
    list_display = ["chat_id", "role"]
    list_filter = [
        "role",
    ]


@admin.register(ProductIncome)
class ProductIncomeAdminClass(ModelAdmin):
    list_display = ["product_template", "number_of_products", "price"]


@admin.register(ProductOutcome)
class ProductOutcomeAdminClass(ModelAdmin):
    list_display = ["product_template", "number_of_products", "sold_price"]


@admin.register(ProductTemplate)
class ProductTemplateAdminClass(ModelAdmin):
    list_display = ["title", "volume_liters", "number_of_products"]
