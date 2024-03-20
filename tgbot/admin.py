from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db import models
from unfold.admin import ModelAdmin, TabularInline
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
    Curier,
    UserSubscription,
)

admin.site.unregister(User)


class UserSubscriptionAdmin(TabularInline):
    model = UserSubscription
    exclude = ["activation_date", "number_of_available_products"]
    extra = 1


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


@admin.register(Curier)
class CurierAdminClass(ModelAdmin):
    list_display = ["full_name", "car_model", "phone_number", "phone_numbers_2"]


@admin.register(Referral)
class ReferralAdminClass(ModelAdmin):
    pass


@admin.register(Account)
class AccountAdminClass(ModelAdmin):
    list_display = ["type", "name", "formatted_balance"]

    def formatted_balance(self, obj):
        return f"{obj.balance:,}"

    formatted_balance.short_description = "Mavjud Summa"


@admin.register(Order)
class OrderAdminClass(ModelAdmin):
    list_display = ["customer", "status", "number_of_products", "created_at"]
    list_filter = ["status"]


@admin.register(InOutCome)
class InOutComeAdminClass(ModelAdmin):
    list_display = ["account", "formatted_amount", "status", "date_added"]

    def formatted_amount(self, obj):
        return f"{obj.amount:,}"

    formatted_amount.short_description = "Amount"


@admin.register(Promotion)
class PromotionAdminClass(ModelAdmin):
    list_display = ["number_of_stars", "formatted_price"]

    def formatted_price(self, obj):
        return f"{obj.winning_price:,}"

    formatted_price.short_description = "Bonus summa"


@admin.register(Subscription)
class SubscriptionAdminClass(ModelAdmin):
    list_display = ["title", "formatted_cost", "product_count", "bonus"]

    def formatted_cost(self, obj):
        return f"{obj.cost:,}"

    formatted_cost.short_description = "Sotilish narxi"


@admin.register(TelegramUser)
class TelegramUserAdminClass(ModelAdmin):
    list_display = ["phone_number", "role", "payment_type", "is_active"]
    list_filter = [
        "role",
    ]
    search_fields = ["phone_number"]
    inlines = [UserSubscriptionAdmin]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.exclude(role=3)
        return queryset


@admin.register(ProductInOut)
class ProductInOutAdminClass(ModelAdmin):
    list_display = ["product_template", "number_of_products", "status"]


@admin.register(ProductTemplate)
class ProductTemplateAdminClass(ModelAdmin):
    list_display = ["title", "volume_liters", "number_of_products"]
