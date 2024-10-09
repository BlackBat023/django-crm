from django import forms
from .models import Orders
import random

class OrderForm(forms.ModelForm):
    MOP_CHOICES = [
        ('Cash', 'Cash'),
        ('EFT', 'EFT'),
        ('Credit Card', 'Credit Card'),
    ]

    PRODUCT_CHOICES = [
        ("Rooikrans", "Rooikrans"),
        ('Black Wattle', 'Black Wattle'),
        ('Bloekom', 'Bloekom'),
        ('Myrtle', 'Myrtle'),
        ('Kameeldoring lg', 'Kameeldoring lg'),
        ('Kameeldoring sm', 'kameeldoring sm'),
        ('Swart haak lg', 'Swart haak lg'),
        ('Swart haak sm', 'Swart haak sm'),
        ('Rooikrans 26pcs bag', 'Rooikrans 26pcs bag'),
        ('Rooikrans 12pcs bag', 'Rooikrans 12pcs bag'),
        ('Black Wattle 26pcs bag', 'Black Wattle 26pcs bag'),
        ('Bloekom 26pcs bag', 'Bloekom 26pcs bag'),
        ('Starters', 'Starters'),
        ('Blitz', 'Blitz'),
    ]

    PAYMENT_CHOICES = [
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
    ]

    product = forms.ChoiceField(choices=PRODUCT_CHOICES, required=True, widget=forms.widgets.Select(attrs={'class':'form-control'}))

    mop = forms.ChoiceField(choices=MOP_CHOICES, required=True)

    payment_status = forms.ChoiceField(choices=PAYMENT_CHOICES, required=True)
    class Meta:
        model = Orders
        order_nr = random.randint(1000, 9999)
        fields = ['date', 'product', 'unit_price', 'qty', 'delivery_fee', 'notes', 'mop', 'payment_status', 'payment_date', 'order_num']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control'}),
            'payment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'order_num': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'value': order_nr}),
        }
