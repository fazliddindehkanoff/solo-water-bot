# Generated by Django 4.0.3 on 2024-07-21 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0050_remove_telegramuser_bonus_balance_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='cashback_for_referer',
            field=models.IntegerField(default=0, verbose_name='Taklif qilgan foydalanuvchi uchun bonus summasi'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='cashback_amount',
            field=models.IntegerField(default=0, verbose_name='Referalning har bir xaridlaridan olinadigan cashback narxi'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='cashback_percent',
            field=models.IntegerField(verbose_name='Keyingi xaridlari uchun cashback foizi'),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='bonus_in_percent',
            field=models.IntegerField(default=0, verbose_name='Donalab sotib olish uchun bonus foizi'),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='cashback',
            field=models.BigIntegerField(default=0, verbose_name='cashback summasi'),
        ),
    ]
