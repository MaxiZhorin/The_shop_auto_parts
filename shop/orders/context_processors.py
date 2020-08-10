from .models import ProductInBasket
from products.models import *
from django.contrib.auth import authenticate

def getting_basket_info(request):

    session_key = request.session.session_key
    if not session_key:
        #workaround for newer Django versions
        # print('sesion keyyyyyy12313121231')
        request.session["session_key"] = 123
        #re-apply value
        # request.session.cycle_key()

    users = request.user
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)
    products_total_nmb = products_in_basket.count()
    group_parse = ProductGroup.objects.filter(is_active=True)
    total_price = 0
    for total in products_in_basket:
        total_price = total_price +(total.price_per_item * total.nmb)


    return locals()