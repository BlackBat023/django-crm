# orders/models.py
from django.db import models
from core.models import Clients
from django.utils import timezone

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

    def get_item_names(self):
        return ", ".join([item.item_name for item in self.orderitem_set.all()])
    
    def get_total_quantity(self):
        return sum(item.quantity for item in self.orderitem_set.all())

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


class Invoice(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='invoices')
    invoice_number = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    due_date = models.DateField()
    paid = models.BooleanField(default=False)
    pdf_file = models.FileField(upload_to='invoices/', null=True, blank=True)

    def __str__(self):
        return f"Invoice {self.invoice_number} for Order {self.order.id}"
    