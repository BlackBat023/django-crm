# Generated by Django 5.1 on 2024-11-29 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0021_remove_order_invoices_order_invoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
