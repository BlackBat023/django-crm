# Generated by Django 5.1 on 2024-11-28 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0018_order_invoice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='invoice',
        ),
    ]
