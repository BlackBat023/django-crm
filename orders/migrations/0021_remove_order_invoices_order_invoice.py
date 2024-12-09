# Generated by Django 5.1 on 2024-11-29 23:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0020_remove_invoice_order_order_invoices_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='invoices',
        ),
        migrations.AddField(
            model_name='order',
            name='invoice',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.invoice'),
        ),
    ]
