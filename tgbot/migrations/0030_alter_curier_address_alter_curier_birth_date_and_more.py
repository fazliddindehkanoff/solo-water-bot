# Generated by Django 4.0.3 on 2024-03-05 05:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0029_alter_order_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curier',
            name='address',
            field=models.TextField(null=True, verbose_name='Manzil'),
        ),
        migrations.AlterField(
            model_name='curier',
            name='birth_date',
            field=models.DateField(null=True, verbose_name='Date of Birth'),
        ),
        migrations.AlterField(
            model_name='curier',
            name='car_license_plate',
            field=models.CharField(max_length=255, null=True, verbose_name='Mashina davlat raqami'),
        ),
        migrations.AlterField(
            model_name='curier',
            name='car_model',
            field=models.CharField(max_length=255, null=True, verbose_name='Mashina modeli'),
        ),
        migrations.AlterField(
            model_name='curier',
            name='chat_id',
            field=models.CharField(max_length=255, null=True, verbose_name='Chat ID'),
        ),
        migrations.AlterField(
            model_name='curier',
            name='full_name',
            field=models.CharField(max_length=255, null=True, verbose_name="To'liq ismi"),
        ),
        migrations.AlterField(
            model_name='curier',
            name='passport_data',
            field=models.CharField(max_length=255, null=True, verbose_name="Passport ma'lumotlari"),
        ),
        migrations.AlterField(
            model_name='curier',
            name='phone_number',
            field=models.CharField(max_length=20, null=True, verbose_name='Telefon raqami'),
        ),
        migrations.AlterField(
            model_name='curier',
            name='phone_numbers_2',
            field=models.CharField(max_length=255, null=True, verbose_name='2 chi telefon raqami'),
        ),
        migrations.AlterField(
            model_name='order',
            name='curier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_orders', to='tgbot.telegramuser', verbose_name='Kurier'),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='role',
            field=models.IntegerField(choices=[(1, 'Admin'), (2, 'Foydalanuvchi'), (3, 'Kurier')], default=2, verbose_name='Rol'),
        ),
    ]
