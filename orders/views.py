from django.shortcuts import render, redirect
from .models import Orders
from core.models import Clients
from django.contrib import messages
from .forms import OrderForm


# Create your views here.
def daily_orders(request):
    clients = Clients.objects.all()
    orders = Orders.objects.all()

    context = {
        "clients": clients,
        "orders": orders,
    }

    return render(request, 'daily_orders.html', context)

def cart(request):
    cart = request.session.get('cart', {})
    return render(request, 'add_orders.html', {'cart': cart})

def add_order(request, client_id):
  if request.method == 'POST':
    form = OrderForm(request.POST)
    
    if form.is_valid():
      order = form.save(commit=False)
      order.client = request.clients.id
      # Save the order
      order.total_price = order.qty * order.unit_price
      order.save()
      messages.success(request, 'Order added successfully')
      return redirect('core:home.html')
  else:
     form = OrderForm()
  return render(request, 'add_orders.html', {'form': form})     
  