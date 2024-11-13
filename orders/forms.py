# orders/forms.py
from django import forms
from .models import Order, OrderItem, Invoice
from django.forms import inlineformset_factory

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('client', 'order_date', 'total_cost', 'payment_status', 'method_of_payment')
        widgets = {
            'client': forms.TextInput(attrs={'readonly': 'readonly'}),
            'order_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-controll'}),
            'total_cost': forms.NumberInput(attrs={'readonly': 'readonly'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args,**kwargs)
        self.fields['total_cost'].required = False

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ('item_name', 'quantity', 'unit_price', 'total_price')
        widgets = {
            'item_name': forms.Select(attrs={'class': 'form-controll'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-controll'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-controll'}),
            'total_price': forms.NumberInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        self.fields['total_price'].widget.attrs['readonly'] = True
        self.fields['total_price'].required = False

    def clean_total_price(self):
        unit_price = self.cleaned_data.get('unit_price', 0)
        quantity = self.cleaned_data.get('quantity', 0)
        delivery_price = self.cleaned_data.get('delivery_price', 0)
        return unit_price * quantity + delivery_price
    
OrderItemFormSet = inlineformset_factory(
    Order, OrderItem,
    fields=('id', 'item_name', 'quantity', 'unit_price', 'delivery_price', 'total_price'),
    extra=1, can_delete=True
)

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['due_date']
    