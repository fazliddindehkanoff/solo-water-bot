ROLE_CHOICES = [
    (1, "Admin"),
    (2, "Foydalanuvchi"),
]


ACCOUNT_TYPE_CHOICES = [
    (1, "Naqd"),
    (2, "Karta"),
    (3, "Qarz"),
    (4, "O'tkazma"),
]

SALES_CHOICES = [
    (1, "Sotib olish"),
    (2, "Sotish"),
]

INOUTCOME_CHOICES = [
    (1, "Kirim"),
    (2, "Chiqim"),
]

ORDER_STATUS_CHOICES = [
    (1, "Aktiv buyurtma"),
    (2, "Bajarildi"),
    (3, "Bekor qilindi"),
]

NUM_EMOJIS = {
    1: "1️⃣",
    2: "2️⃣",
    3: "3️⃣",
    4: "4️⃣",
    5: "5️⃣",
    6: "6️⃣",
    7: "7️⃣",
    8: "8️⃣",
    9: "9️⃣",
    10: "🔟",
}


PAYMENT_CHOICES = [
    (1, "Karta orqali"),
    (2, "Naqd orqali"),
]

PAYMENT_STATUS_CHOICES = [
    (1, "To'lov qilmadi"),
    (2, "To'lov kutilmoqda"),
    (3, "To'lov qilindi"),
]

MAIN_MENU_BTNS = {
    "my_details": "📜 Mening buyurtmalar tarixim",
    "order": "🚚 Buyurtma berish",
    "my_referal_link": "🔗 Referal link olish",
    "my_referals": "👥Referallarim",
    "contact_with_operator": "📱 Operator bilan aloqa",
    "subscriptions": "🧾 Tarif",
}
