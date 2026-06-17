from django.shortcuts import render, get_object_or_404
from .models import (
    Customer, 
    PaintProduct, PaintInvoice, PaintInvoiceItem,
    ElectricalProduct, ElectricalInvoice, ElectricalInvoiceItem # <-- Make sure these are here!
)
import json
from django.http import JsonResponse
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, F
# Create your views here.

@login_required
def home(request):
    today = timezone.now().date()
    start_of_day = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
    end_of_day = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.max.time()))
    paint_revenue = PaintInvoice.objects.filter(date_created__range=(start_of_day, end_of_day)).aggregate(Sum('final_amount'))['final_amount__sum'] or 0
    elec_revenue = ElectricalInvoice.objects.filter(date_created__range=(start_of_day, end_of_day)).aggregate(Sum('final_amount'))['final_amount__sum'] or 0
    total_revenue_today = paint_revenue + elec_revenue
    paint_bills = PaintInvoice.objects.filter(date_created__range=(start_of_day, end_of_day)).count()
    elec_bills = ElectricalInvoice.objects.filter(date_created__range=(start_of_day, end_of_day)).count()
    total_bills_today = paint_bills + elec_bills
    paint_low_stock = PaintProduct.objects.filter(stock_quantity__lte=F('low_stock_threshold')).count()
    elec_low_stock = ElectricalProduct.objects.filter(stock_quantity__lte=F('low_stock_threshold')).count()
    total_low_stock = paint_low_stock + elec_low_stock

    return render(request, 'billing/home.html', {
        'current_page': 'home',
        'total_revenue_today': total_revenue_today,
        'total_bills_today': total_bills_today,
        'total_low_stock': total_low_stock,
    })

@login_required
def paint_pos(request):
    products = PaintProduct.objects.all()
    customers = Customer.objects.all()

    return render(request, 'billing/paint_pos.html', {
        'products': products,
        'shop_type': 'paint',     # NEW
        'current_page': 'pos'     # NEW
    })

@login_required
def electrical_pos(request):
    products = ElectricalProduct.objects.all()
    customers = Customer.objects.all()
    
    return render(request, 'billing/electrical_pos.html', {
        'products': products,
        'shop_type': 'electrical', # NEW
        'current_page': 'pos'      # NEW
    })

@csrf_exempt
def paint_checkout(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cart = data.get('cart', [])
            discount = float(data.get('discount', 0))
            
            # 1. Grab the real customer data from JavaScript!
            c_phone = data.get('customer_phone')
            c_name = data.get('customer_name')

            if not c_phone or not c_name:
                raise Exception("Customer Name and Phone Number are required!")

            # 2. Find the customer, or create a new one automatically!
            with transaction.atomic():
                customer, created = Customer.objects.get_or_create(
                    phone_number=c_phone,
                    defaults={'name': c_name}
                )

                # Calculate totals...
                sub_total = sum(float(item['price']) * int(item['qty']) for item in cart)
                final_amount = sub_total - discount

                # Create the Master Bill using the REAL customer
                invoice = PaintInvoice.objects.create(
                    invoice_number=f"PT-100{PaintInvoice.objects.count() + 1}",
                    customer=customer,
                    sub_total=sub_total,
                    discount_amount=discount,
                    final_amount=final_amount
                )

                # ... (The rest of your item looping and stock deduction stays exactly the same!) ...
                for item in cart:
                    product = PaintProduct.objects.get(id=item['id'])
                    if product.stock_quantity < item['qty']:
                        raise Exception(f"Not enough stock for {product.name}!")
                    
                    product.stock_quantity -= item['qty']
                    product.save()

                    PaintInvoiceItem.objects.create(
                        invoice=invoice,
                        product=product,
                        quantity=item['qty'],
                        price_at_sale=item['price']
                    )

            return JsonResponse({'message': 'Success', 'invoice_id': invoice.id})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@login_required
def paint_history(request):
    query = request.GET.get('q','')
    invoices = PaintInvoice.objects.all().order_by('-date_created')

    if query:
        invoices = invoices.filter(
            Q(invoice_number__icontains=query) | 
            Q(customer__phone_number__icontains=query) |
            Q(customer__name__icontains=query)
        )
    return render(request, 'billing/paint_history.html', {
        'invoices': invoices,
        'query': query,
        'shop_type': 'paint',     # NEW
        'current_page': 'ledger'  # NEW
    })

@login_required
def paint_receipt(request, invoice_id):
    invoice = get_object_or_404(PaintInvoice, id=invoice_id)
    items = PaintInvoiceItem.objects.filter(invoice=invoice)

    # NEW: Calculate the exact CGST and SGST for the printed receipt
    total_tax = 0
    for item in items:
        item_total = item.price_at_sale * item.quantity
        base_price = float(item_total) / (1 + (float(item.product.gst_rate) / 100))
        total_tax += (float(item_total) - base_price)
    
    # Split the tax in half for Central and State
    cgst = total_tax / 2
    sgst = total_tax / 2

    return render(request, 'billing/paint_receipt.html', {
        'invoice': invoice,
        'items': items,
        'cgst': cgst,   # NEW
        'sgst': sgst,   # NEW
    })

@csrf_exempt
def electrical_checkout(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cart = data.get('cart', [])
            discount = float(data.get('discount', 0))
            
            # 1. Grab the real customer data
            c_phone = data.get('customer_phone')
            c_name = data.get('customer_name')

            if not c_phone or not c_name:
                raise Exception("Customer Name and Phone Number are required!")

            with transaction.atomic():
                # 2. Find or Create the Customer
                customer, created = Customer.objects.get_or_create(
                    phone_number=c_phone,
                    defaults={'name': c_name}
                )

                sub_total = sum(float(item['price']) * int(item['qty']) for item in cart)
                final_amount = sub_total - discount

                # 3. Create the Electrical Master Bill (Notice the EL- prefix!)
                invoice = ElectricalInvoice.objects.create(
                    invoice_number=f"EL-100{ElectricalInvoice.objects.count() + 1}",
                    customer=customer,
                    sub_total=sub_total,
                    discount_amount=discount,
                    final_amount=final_amount
                )

                for item in cart:
                    product = ElectricalProduct.objects.get(id=item['id'])
                    if product.stock_quantity < item['qty']:
                        raise Exception(f"Not enough stock for {product.name}!")

                    product.stock_quantity -= item['qty']
                    product.save()

                    ElectricalInvoiceItem.objects.create(
                        invoice=invoice,
                        product=product,
                        quantity=item['qty'],
                        price_at_sale=item['price']
                    )

            return JsonResponse({'message': 'Success', 'invoice_id': invoice.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@login_required
def electrical_history(request):
    query = request.GET.get('q', '')
    invoices = ElectricalInvoice.objects.all().order_by('-date_created')

    if query:
        invoices = invoices.filter(
            Q(invoice_number__icontains=query) | 
            Q(customer__phone_number__icontains=query) |
            Q(customer__name__icontains=query)
        )

    return render(request, 'billing/electrical_history.html', {
        'invoices': invoices,
        'query': query,
        'shop_type': 'electrical', # NEW
        'current_page': 'ledger'   # NEW
    })

@login_required
def electrical_receipt(request, invoice_id):
    invoice = get_object_or_404(ElectricalInvoice, id=invoice_id)
    items = invoice.items.all()

    return render(request, 'billing/electrical_receipt.html', {
        'invoice': invoice,
        'items': items
    })

@login_required
def add_product(request):
    success_message = None
    current_shop = request.GET.get('shop', 'shared') 


    if request.method == 'POST':
        shop_type = request.POST.get('shop_type')
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        threshold = request.POST.get('threshold')

        if shop_type == 'paint':
            PaintProduct.objects.create(
                name=name, price=price, stock_quantity=stock, 
                low_stock_threshold=threshold
            )
            success_message = f"Success! {name} added to Paint Inventory."
            
        elif shop_type == 'electrical':
            ElectricalProduct.objects.create(
                name=name, price=price, stock_quantity=stock, 
                low_stock_threshold=threshold
            )
            success_message = f"Success! {name} added to Electrical Inventory."

    return render(request, 'billing/add_product.html', {
        'success_message': success_message,
        'shop_type': current_shop,   # NEW
        'current_page': 'inventory'  # NEW
    })

@login_required
def manage_inventory(request):
    # Figure out which shop we are managing from the URL (default to paint)
    shop_type = request.GET.get('shop', 'paint') 
    
    if shop_type == 'paint':
        products = PaintProduct.objects.all().order_by('name')
    else:
        products = ElectricalProduct.objects.all().order_by('name')
        
    return render(request, 'billing/manage_inventory.html', {
        'products': products,
        'shop_type': shop_type,
        'current_page': 'manage'
    })

@csrf_exempt
def update_inventory_item(request):
    # This is a silent API endpoint that JavaScript talks to!
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_id = data.get('id')
            shop_type = data.get('shop_type')
            new_price = float(data.get('price'))
            new_stock = int(data.get('stock'))

            # Update the correct database table
            if shop_type == 'paint':
                product = PaintProduct.objects.get(id=item_id)
            elif shop_type == 'electrical':
                product = ElectricalProduct.objects.get(id=item_id)

            product.price = new_price
            product.stock_quantity = new_stock
            product.save()

            return JsonResponse({'message': 'Success'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)