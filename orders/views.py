# orders/views.py
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib import messages
from django.template.loader import render_to_string
from django.forms import inlineformset_factory
from .forms import OrderForm, OrderItemForm, OrderItemFormSet, InvoiceForm
from .models import Order, OrderItem, Invoice
from core.models import Clients
from django.db.models import Prefetch
import json
import weasyprint
from weasyprint import HTML
from django.http import JsonResponse, HttpResponse
from django.db import transaction
from datetime import datetime
import tempfile

logger = logging.getLogger('orders')

@login_required
def order_list(request):
    clients = Clients.objects.all()
    orders = Order.objects.all().select_related('client').prefetch_related(
        Prefetch('invoice', queryset=Invoice.objects.all())
    )
    # invoices = Order.objects.prefetch_related('invoices').all()

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    # Get all clients
    client_id = request.GET.get('client_id')

    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        orders = orders.filter(order_date__gte=start_date)
    
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        orders = orders.filter(order_date__lte=end_date)

    # Get all orders
    if client_id:
        orders = orders.filter(client_id=client_id)
    else:
        orders = orders.all()
    
    context = {
        'orders': orders,
        'clients': clients,
        # 'invoices': invoices,
    }
    return render(request, 'order_list.html', context)

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
@require_POST
def order_delete(request, pk):
    if request.method == 'POST':
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        messages.success(request, 'Order deleted successfully')
        return redirect('orders:order_list.html')
    else:
        return render(request, 'orders:order_delete_confirm.html', {'order': order})

@login_required
def generate_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.order = order
            invoice.invoice_number = f"INV-{order.id}-{Invoice.objects.count() + 1}"

            # Generate the PDF file
            html_string = render_to_string('invoice_template.html', {'order': order, 'invoice': invoice})
            html = HTML(string=html_string)
            result = html.write_pdf()

            # Save PDF to temporary file
            with tempfile.NamedTemporaryFile(delete=False) as output:
                output.write(result)
                temp_file = output.name

            # Save the invoice with PDF file
            invoice.pdf_file.save(f"{invoice.invoice_number}.pdf", open(temp_file, 'rb'))
            invoice.save()

            # Set the invoice field of the Order object
            order.invoice = invoice
            order.save()

            return redirect('orders:invoice_detail', invoice_id=invoice.id)
    else:
        form = InvoiceForm()

    return render(request, 'generate_invoice.html', {'form': form, 'order': order})

@login_required
def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    return render(request, 'invoice_detail.html', {'invoice': invoice})

def print_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    if invoice.pdf_file:
        with open(invoice.pdf_file.path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline;filename={invoice.invoice_number}.pdf'
            return response
        
    return HttpResponse("PDF not found", status=404)