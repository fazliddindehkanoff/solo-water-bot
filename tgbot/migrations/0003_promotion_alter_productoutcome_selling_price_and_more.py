# Generated by Django 4.0.3 on 2024-02-15 20:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0002_producttemplate_telegramuser_role_productoutcome_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_stars', models.IntegerField()),
                ('winning_price', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='productoutcome',
            name='selling_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('product_count', models.IntegerField()),
                ('bonus', models.IntegerField()),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tgbot.producttemplate')),
            ],
        ),
    ]
