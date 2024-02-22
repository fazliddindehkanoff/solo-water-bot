# Generated by Django 4.0.3 on 2024-02-22 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0016_telegramuser_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='telegramuser',
            name='payment_type',
            field=models.IntegerField(choices=[(1, 'Karta orqali'), (2, 'Naqd orqali')], default=1),
            preserve_default=False,
        ),
    ]