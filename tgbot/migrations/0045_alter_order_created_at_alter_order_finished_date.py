# Generated by Django 4.0.3 on 2024-06-06 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0044_alter_subscription_options_order_finished_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Buyurtma berilgan vaqti'),
        ),
        migrations.AlterField(
            model_name='order',
            name='finished_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Buyurtma tugatilgan vaqti'),
        ),
    ]
