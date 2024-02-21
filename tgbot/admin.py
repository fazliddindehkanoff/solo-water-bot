from django.contrib import admin
from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import (
    TelegramUser,
    ProductInOut,
    ProductTemplate,
    Promotion,
    Subscription,
    Account,
    Order,
    InOutCome,
)


@admin.register(Account)
class AccountAdminClass(ModelAdmin):
    list_display = ["type", "name", "balance"]


@admin.register(Order)
class OrderAdminClass(ModelAdmin):
    list_display = ["customer", "status", "number_of_products", "created_at"]


@admin.register(InOutCome)
class InOutComeAdminClass(ModelAdmin):
    list_display = ["account", "amount", "status", "date_added"]


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


@admin.register(ProductInOut)
class ProductInOutAdminClass(ModelAdmin):
    list_display = ["product_template", "number_of_products", "status"]


@admin.register(ProductTemplate)
class ProductTemplateAdminClass(ModelAdmin):
    list_display = ["title", "volume_liters", "number_of_products"]
