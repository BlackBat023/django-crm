# orders/models.py
from django.db import models
from core.models import Clients

class Order(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    order_date = models.DateField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=10, default='Pending', choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    ])
    method_of_payment = models.CharField(max_length=10, default='Cash', choices=[
        ('Cash', 'Cash'),
        ('EFT', 'EFT'),
        ('Card', 'Card'),
    ])

    def update_total_cost(self):
        self.total_cost = sum(item.total_price for item in self.orderitem_set.all())
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_price = (self.unit_price * self.quantity) + self.delivery_price
        super().save(*args, **kwargs)
        self.order.update_total_cost()