# orders/views.py
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.forms import inlineformset_factory
from .forms import OrderForm, OrderItemForm, OrderItemFormSet
from .models import Order, OrderItem
from core.models import Clients
import json
from django.http import JsonResponse
from django.db import transaction

logger = logging.getLogger('orders')

@login_required
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'order_list.html', {'orders': orders})

@login_required
def order_detail(request, pk):
    order = Order.objects.get(pk=pk)
    print(order)
    return render(request, 'order_detail.html', {'order': order})

@login_required
@ require_http_methods(["GET", "POST"])
def order_create(request, client_id):
    client = get_object_or_404(Clients, id=client_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():  # Wrap the transaction in a block
                    order = form.save(commit=False)
                    order.client = client
                    order.save()  # Save the order first

                    # Parse the JSON data from the request
                    items_data = json.loads(request.POST.get('items_data', '[]'))
                    logger.info(f"Received items_data: {items_data}")

                    order_items = []
                    for item_data in items_data:
                        order_item = OrderItem(
                            order=order,  # Use the saved order
                            item_name=item_data['item_name'],
                            quantity=int(item_data['quantity']),
                            unit_price=float(item_data['unit_price']),
                            delivery_price=float(item_data['delivery_price']),
                            total_price=float(item_data['total_price'])
                        )
                        order_items.append(order_item)
                    
                    #Bulk create order items
                    OrderItem.objects.bulk_create(order_items)

                    # Update order total cost
                    order.update_total_cost()

                return JsonResponse({'success': True, 'order_id': order.pk})
            except Exception as e:
                logger.error(f"Error in order_create: {str(e)}", exc_info=True)
                return JsonResponse({'success': False, 'errors': str(e)}, status=500)
        else:
            logger.error(f"Form validation errors: {form.errors}")
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = OrderForm(initial={'client': client})

    return render(request, 'order_form.html', {'form': form, 'client': client})


@login_required
def order_item_create(request, pk):
    order = Order.objects.get(pk=pk)
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            order_item = form.save(commit=False)
            order_item.order = order
            order_item.save()
            return redirect('orders:order_detail', pk=order.pk)
    else:
        form = OrderItemForm()
    return render(request, 'order_item_form.html', {'form': form})

@login_required
def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        formset = OrderItemFormSet(request.POST, instance=order)
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic(): # Wrap the transaction in a block
                    form.save()
                    formset.save()
                    order.update_total_cost()
                messages.success(request, "Order updated successfully!")
                return redirect('orders:order_detail', pk=order.pk)
            except Exception as e:
                messages.error(request, f"An Error has occurred: {str(e)}")
        else:
            print("Form errors:", form.errors)
            print("Formset errors:", formset.errors)
            messages.error(request, "Form validation errors: {form.errors}, {formset.errors}")
    else:
        form = OrderForm(instance=order)
        formset = OrderItemFormSet(instance=order)
    return render(request, 'order_update.html', {'form': form, 'formset': formset, 'order': order})

@login_required
def order_delete(request, pk):
    delete_order = get_object_or_404(Order, pk=pk)
    delete_items = OrderItem.objects.filter(order=delete_order)

    # Delete the items first
    delete_items.delete()
    # Delete the order
    delete_order.delete()
    
    messages.success(request, "Order successfully deleted...")
    return redirect('orders:order_list.html')
