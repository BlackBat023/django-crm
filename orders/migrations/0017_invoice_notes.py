# Generated by Django 5.1 on 2024-11-15 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0016_invoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='notes',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
