from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db import models
from unfold.admin import ModelAdmin
from unfold.forms import UserCreationForm, UserChangeForm, AdminPasswordChangeForm
from unfold.contrib.forms.widgets import WysiwygWidget


from .models import (
    TelegramUser,
    ProductInOut,
    ProductTemplate,
    Promotion,
    Subscription,
    Account,
    Order,
    InOutCome,
    Referral,
)

admin.site.unregister(User)


@admin.register(User)
class UserAdminClass(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }
    list_display = [
        "username",
        "is_staff",
    ]


@admin.register(Referral)
class ReferralAdminClass(ModelAdmin):
    pass


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
    list_display = ["phone_number", "role", "payment_type", "is_active"]
    list_filter = [
        "role",
    ]
    search_fields = ["phone_number"]


@admin.register(ProductInOut)
class ProductInOutAdminClass(ModelAdmin):
    list_display = ["product_template", "number_of_products", "status"]


@admin.register(ProductTemplate)
class ProductTemplateAdminClass(ModelAdmin):
    list_display = ["title", "volume_liters", "number_of_products"]
