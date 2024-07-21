# Generated by Django 4.0.3 on 2024-07-13 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0047_alter_telegramuser_available_bottles'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='bonus',
        ),
        migrations.AddField(
            model_name='subscription',
            name='cashback_percent',
            field=models.IntegerField(default=0, verbose_name='Keyingi tarif xaridlari uchun kashbak foizi'),
            preserve_default=False,
        ),
    ]