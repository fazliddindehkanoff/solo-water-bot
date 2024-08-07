# Generated by Django 4.0.3 on 2024-06-01 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0036_remove_inoutcome_status_inoutcome_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='chat_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='full_name',
            field=models.CharField(blank=True, default='', max_length=250, verbose_name="To'liq ism"),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='state',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
