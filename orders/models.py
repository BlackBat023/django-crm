from django.db import models

# Create your models here.
class Orders(models.Model):

    client_id = models.ForeignKey('core.Clients', on_delete=models.CASCADE)
    date = models.DateField()
    product = models.CharField(max_length=100)
    unit_price=models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.IntegerField()
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.CharField(max_length=400)
    mop = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=50)
    payment_date = models.DateField(null=True, blank=True)
    order_num = models.CharField(max_length=50, unique=True)

