from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from .models import *
from django.shortcuts import render

from .forms import CheckoutContactForm
from django.contrib.auth.models import User
from utils.emails import SendingEmail


def basket_adding(request):
    return_dict = dict()
    session_key = request.session.session_key
    print(request.POST)
    data = request.POST
    product_id = data.get("product_id")
    nmb = data.get("nmb")
    is_delete = bool(data.get("is_delete"))

    if is_delete == True:
        ProductInBasket.objects.filter(id=product_id).update(is_active=False)
    else:
        new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key, product_id=product_id,is_active=True, defaults={'nmb': nmb})
        if not created:
            print("not created")
            new_product.nmb += int(nmb)
            new_product.save(force_update=True)

    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)
    products_total_nmb = products_in_basket.count()
    return_dict["products_total_nmb"] = products_total_nmb
    return_dict["products"] = list()
    print('views',products_in_basket)

    for item in products_in_basket:
        product_dict = dict()
        product_dict["id"] = item.id
        product_dict["name"] = item.product.customer_name
        product_dict["price"] = item.product.price
        product_dict["price_per_item"] = item.price_per_item
        product_dict["nmb"] = int(item.nmb)
        product_dict["is_active"] = item.is_active
        return_dict["products"].append(product_dict)

    return JsonResponse(return_dict)


def checkout(request):
    session_key = request.session.session_key
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    form = CheckoutContactForm(request.POST or None)
    if request.POST:
        print(request.POST)
        if form.is_valid():
            data = request.POST
            username = data.get('User')
            print("yes")
            name = data.get("name")
            phone = data["phone"]
            email =data["email"]
            biling = data["ship"]
            shiping = int(data["ship1"])
            commit = data["commit"]

            if shiping == 0:
                shiping = 'самовывоз'
            elif shiping == 200:
                shiping = 'TK'
            elif shiping == 400:
                shiping = 'Почта'
            user, created = User.objects.get_or_create(username=username)
            order = Order.objects.create(customer_fio=name,customer_email=email,customer_adress=biling,
                                         customer_name=user, customer_phone=phone, status_id=1,
                                         ship_metod=shiping, comments=commit)
            for name, value in data.items():
                if name.startswith("product_in_basket_"):
                    product_in_basket_id = name.split("product_in_basket_")[1]
                    product_in_basket = ProductInBasket.objects.get(id=product_in_basket_id)
                    product_in_basket.nmb = int(value)
                    product_in_basket.order = order
                    product_in_basket.save(force_update=True)

                    ProductInOrder.objects.create(product=product_in_basket.product, nmb=product_in_basket.nmb,
                                                  price_per_item=product_in_basket.price_per_item,
                                                  total_price=product_in_basket.total_price,order=order)
                    ProductInBasket.objects.filter(id=product_in_basket_id).update(is_active=False)

            email = SendingEmail()
            email.sending_email(type_id=1, order=order)
            email.sending_email(type_id=2, email=order.customer_email, order=order)

            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            print("no")
    return render(request, 'orders/checkout.html', locals())

