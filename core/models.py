from django.db import models

# Create your models here.
class Clients(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contact = models.CharField(max_length=10)
    address = models.CharField(max_length=200)
    area = models.CharField(max_length=200)
    suburb = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return(f"{self.first_name} {self.last_name}")