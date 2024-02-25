from datetime import datetime

from tgbot.models import Order


def custom_context(request):
    # Get today's date
    today = datetime.now().date()

    # Filter orders created today
    today_orders = Order.objects.filter(created_at__date=today)

    # Count the number of today's orders
    today_orders_count = today_orders.count()

    # Filter closed orders created today
    closed_today_orders = today_orders.filter(status=2)

    # Count the number of closed orders created today
    today_closed_orders_count = closed_today_orders.count()

    # Count the number of unique customers who placed orders today
    today_orders_customer_count = today_orders.values("customer").distinct().count()

    return {
        "today_orders": today_orders,
        "today_orders_count": today_orders_count,
        "today_closed_orders_count": today_closed_orders_count,
        "today_orders_customer_count": today_orders_customer_count,
    }
