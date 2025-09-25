from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Order, OrderUpdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

# Import Paytm checksum
import paytmchecksum

# Staging Merchant Key (Demo)
PAYTM_MERCHANT_KEY = 'kbzk5y3adk7!bpkz'

# Shop Homepage
def shop(request):
    products = Product.objects.all()
    allProds = []  
    cats = {prod.category for prod in products}

    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nslides = n // 3 + ceil((n / 3) - (n // 3))
        chunks = [prod[i:i+3] for i in range(0, n, 3)]
        allProds.append([chunks, nslides, cat])

    params = {"allProds": allProds}
    return render(request, "shop/index.html", params)
from django.db.models import Q

def search(request):
    query = request.GET.get("query", "")
    results = []

    if query:
        results = Product.objects.filter(
            Q(product_name__icontains=query) | Q(description__icontains=query)
        )

    context = {
        "query": query,
        "results": results  # make sure key name matches template usage
    }

    return render(request, "shop/p.html", context)


# About page
def about(request):
    return render(request, "shop/about.html")

# Tracker page
def tracker(request):
    updates = []
    order = None
    order_items = []
    error_message = ""

    if request.method == "POST":
        orderid = request.POST.get("orderid", "")
        email = request.POST.get("email", "")

        if orderid and email:
            try:
                order = Order.objects.get(order_id=orderid, email=email)
                updates = OrderUpdate.objects.filter(order_id=orderid).order_by("timstamps")

                if order.items_json:
                    try:
                        items_dict = json.loads(order.items_json)
                        order_items = []
                        for key, val in items_dict.items():
                            order_items.append({
                                "name": val.get("name"),
                                "quantity": val.get("qty"),
                                "price": val.get("price")
                            })
                    except json.JSONDecodeError:
                        error_message = "Order items data is corrupted."
            except Order.DoesNotExist:
                error_message = "Sorry! We can't find your order with the given details."
        else:
            error_message = "Please provide both fields."

    context = {
        "order": order,
        "updates": updates,
        "items": order_items,
        "error_message": error_message
    }

    return render(request, "shop/tracker.html", context)

# Contact page
def contact(request):
    sai=None
    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        desc = request.POST.get("desc", "")
        contact = Contact(name=name, email=email, desc=desc)
        contact.save()
        sai=True
    return render(request, "shop/contact.html",{"sai":sai})

# Product details page
def product(request, myid):
    product = Product.objects.filter(product_id=myid)
    return render(request, "shop/product.html", {"product": product[0]})

# Checkout page
def checkout(request):
    thank=None
    if request.method == "POST":
        items_json = request.POST.get("items_json", "")
        amount = request.POST.get("amount", "1")
        name = request.POST.get("name", "")
        address1 = request.POST.get("address1", "")
        address2 = request.POST.get("address2", "")
        email = request.POST.get("email", "")
        city = request.POST.get("city", "")
        state = request.POST.get("state", "")

        try:
            items_dict = json.loads(items_json)
        except json.JSONDecodeError:
            items_dict = {}

        # Save order
        order = Order(
            items_json=json.dumps(items_dict),
            name=name,
            email=email,
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            amount=amount
        )
        order.save()

        # Initial update
        update = OrderUpdate(order_id=order.order_id, update_desc="Order has been placed")
        update.save()

        # Prepare Paytm parameters
        param_dict = {
            'ORDER_ID': str(order.order_id),
            'CUST_ID': email,
            'TXN_AMOUNT': str(amount),
            'STATUS': 'TXN_SUCCESS'  # Simulate success
        }

        # Generate checksum
        thank=True

        return render(request,"shop/checkout.html",{"thank":thank,"id":order.order_id})

    return render(request, "shop/checkout.html")

# Paytm callback
@csrf_exempt
def RequestHandler(request):
    return HttpResponse("<h1>payment received</h1>")
