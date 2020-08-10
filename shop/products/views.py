from django.shortcuts import render
from .models import *

import django


def product(request,product_id):
    products = Product.objects.get(id=product_id)
    all_cross = ProductCross.objects.filter(product=products)

    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()


    return render(request, 'products/product.html', locals())
