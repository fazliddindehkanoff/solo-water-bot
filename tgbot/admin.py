from datetime import datetime

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db import models
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse

from unfold.admin import ModelAdmin, TabularInline
from unfold.forms import (
    UserCreationForm,
    UserChangeForm,
    AdminPasswordChangeForm,
)
from unfold.contrib.forms.widgets import WysiwygWidget
from unfold.contrib.filters.admin import RangeDateFilter
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
    BonusExchange,
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


@admin.register(BonusExchange)
class BonusExchangeAdminClass(ModelAdmin):
    list_display = [
        "user",
        "ball",
        "comment",
    ]
    autocomplete_fields = ["user"]

    def add_view(self, request, form_url="", extra_context=None):
        if request.method == "POST":
            user_id = request.POST.get("user")
            ball = int(request.POST.get("ball"))
            user_bonus_balance = TelegramUser.objects.get(
                id=user_id
            ).bonus_balance  # noqa
            if user_bonus_balance < ball:
                self.message_user(
                    request,
                    "Tanlangan foydalanuvchida yetarli ball mavjud emas !",
                    level="ERROR",
                )
                return HttpResponseRedirect(
                    reverse("admin:tgbot_bonusexchange_add")
                )  # noqa
            else:
                return super().add_view(request, form_url, extra_context)
        else:
            return super().add_view(request, form_url, extra_context)


@admin.register(Curier)
class CurierAdminClass(ModelAdmin):
    list_display = [
        "full_name",
        "car_model",
        "phone_number",
        "phone_numbers_2",
    ]


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
    list_display = [
        "customer",
        "status",
        "number_of_products",
        "created_at",
        "finished_date",
    ]
    search_fields = ["customer__phone_number"]
    list_filter_submit = True
    list_filter = [
        "status",
        ("created_date", RangeDateFilter),
    ]

    def get_queryset(self, request: HttpRequest) -> models.QuerySet:
        query_params = request.GET.dict()
        from_date_str = query_params.get("created_date_from", None)
        to_date_str = query_params.get("created_date_to", None)
        queryset = super().get_queryset(request)

        date_format = "%d.%m.%Y"  # Desired input format

        if from_date_str:
            try:
                from_date = datetime.strptime(
                    from_date_str,
                    date_format,
                ).date()
                queryset = queryset.filter(created_date__gte=from_date)
            except ValueError:
                # Handle improper date format
                pass

        if to_date_str:
            try:
                to_date = datetime.strptime(to_date_str, date_format).date()
                queryset = queryset.filter(created_date__lte=to_date)
            except ValueError:
                # Handle improper date format
                pass

        return queryset


@admin.register(InOutCome)
class InOutComeAdminClass(ModelAdmin):
    list_display = ["account", "formatted_amount", "date_added"]

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
    list_display = ["title", "formatted_cost", "product_count"]

    def formatted_cost(self, obj):
        return f"{obj.cost:,}"

    formatted_cost.short_description = "Sotilish narxi"


@admin.register(TelegramUser)
class TelegramUserAdminClass(ModelAdmin):
    list_display = [
        "phone_number",
        "role",
        "payment_type",
        "available_bottles",
        "cashback",
        "is_active",
    ]
    exclude = ["state"]
    list_filter = [
        "role",
    ]
    search_fields = ["phone_number"]
    inlines = [UserSubscriptionAdmin]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.exclude(role=3)
        return queryset

    def get_readonly_fields(self, request, obj=None):
        return [
            "chat_id",
            "cashback",
            "available_bottles",
            "bonus_in_percent",
        ]


@admin.register(ProductInOut)
class ProductInOutAdminClass(ModelAdmin):
    list_display = ["product_template", "number_of_products", "status"]


@admin.register(ProductTemplate)
class ProductTemplateAdminClass(ModelAdmin):
    list_display = ["title", "volume_liters", "number_of_products"]
