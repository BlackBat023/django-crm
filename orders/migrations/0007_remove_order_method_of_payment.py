# Generated by Django 5.1 on 2024-10-11 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_order_orderitem_delete_orders'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='method_of_payment',
        ),
    ]