# Generated by Django 5.1 on 2024-10-17 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_alter_orderitem_quantity_alter_orderitem_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='delivery_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]