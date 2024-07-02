# Generated by Django 4.0.3 on 2024-06-02 23:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0039_alter_order_curier'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inoutcome',
            name='client',
        ),
        migrations.AddField(
            model_name='subscription',
            name='cashback_amount',
            field=models.IntegerField(default=0, verbose_name='Kashbak narxi'),
        ),
        migrations.AlterField(
            model_name='order',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tgbot.producttemplate', verbose_name='Maxsulot'),
        ),
    ]
