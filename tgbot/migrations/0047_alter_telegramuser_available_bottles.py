# Generated by Django 4.0.3 on 2024-06-06 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0046_telegramuser_available_bottles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='available_bottles',
            field=models.IntegerField(default=0, verbose_name="Bo'sh idishlar soni"),
        ),
    ]
