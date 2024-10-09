# Generated by Django 5.1 on 2024-09-25 11:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='orders',
            name='delivery_fee',
            field=models.DecimalField(decimal_places=2, default=True, max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='orders',
            name='mop',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='orders',
            name='notes',
            field=models.CharField(max_length=400),
        ),
        migrations.AlterField(
            model_name='orders',
            name='order_num',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='payment_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='payment_status',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='orders',
            name='product',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='orders',
            name='total_cost',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=100)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('qty', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.orders')),
            ],
        ),
    ]