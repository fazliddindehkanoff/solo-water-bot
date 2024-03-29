# Generated by Django 4.0.3 on 2024-02-25 22:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0023_alter_usersubscription_number_of_available_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='curier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_orders', to='tgbot.telegramuser', verbose_name='Kurier'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(1, 'Aktiv buyurtma'), (2, 'Bajarildi'), (3, 'Bekor qilindi')], default=1),
        ),
        migrations.AlterField(
            model_name='order',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='address',
            field=models.CharField(default='', max_length=500, verbose_name='Manzil'),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='bonus_balance',
            field=models.IntegerField(default=0, verbose_name='Bonus ballar'),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='full_name',
            field=models.CharField(default='', max_length=250, verbose_name="To'liq ism"),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Aktivlik xolati'),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='payment_type',
            field=models.IntegerField(choices=[(1, 'Karta orqali'), (2, 'Naqd orqali')], default=0, verbose_name="To'lov turi"),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='phone_number',
            field=models.CharField(default='', max_length=250, verbose_name='Telefon raqam'),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='role',
            field=models.IntegerField(choices=[(1, 'Admin'), (2, 'User')], default=2, verbose_name='Rol'),
        ),
    ]
