# Generated by Django 5.1 on 2024-10-30 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_alter_order_total_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='delivery_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='item_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='total_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]