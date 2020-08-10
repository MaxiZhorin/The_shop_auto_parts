from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from products.models import *


def home(request):
    products = ProductImage.objects.filter(is_active=True, is_main=True)

    products_images = ProductImage.objects.filter(is_active=True, is_main=True)
    products_new = (products_images.order_by('-product__created'))[0:8]
    categories = ProductGroupImage.objects.filter(is_active=True)
    group_parse = ProductGroup.objects.filter(is_active=True)
    return render(request, 'landing/home.html', locals())


def group(request, group_id):
    group_now = ProductGroup.objects.filter(id=group_id)
    group_parse = ProductGroup.objects.filter(is_active=True)
    group_name = group_now[0].name
    products = ProductImage.objects.filter(product__group__name=group_name)
    paginator = Paginator(products,16)
    group=group_id
    print(group)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)
    print(page)

    return render(request,
                  'landing/group_all.html',
                  {'page': page,
                   'products': products,
                   'group':group,
                   'group_name':group_name})

def group_sort(request, group_id,group_sort):
    if group_sort == '1':
        sorting = '-product__price'
    elif group_sort == '2':
        sorting = 'product__price'
    group_now = ProductGroup.objects.filter(id=group_id)
    group_parse = ProductGroup.objects.filter(is_active=True)
    group_name = group_now[0].name
    products = ProductImage.objects.filter(product__group__name=group_name).order_by(sorting)
    paginator = Paginator(products,16)
    group = group_id
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)
    print(page)

    return render(request,
                  'landing/group_all.html',
                  {'page': page,
                   'products': products,
                   'group': group,
                   'group_name': group_name})


def search(request,sort=None):
    data = request.GET.get('f')
    print(sort,'sort')
    if data == None:
        data = ''
    # sorted_by_search = Product.objects.filter(article__exact=data)
    # print(sorted_by_search)
    all_product = ProductImage.objects.filter(is_active=True)
    result = []
    all_name = ProductImage.objects.filter(product__customer_name__istartswith=data)
    all_article = ProductImage.objects.filter(product__article=data)

    ###### поиск по имени
    if all_name:
        for prod in all_name:
            result.append(prod)

    if all_article:
        for prod in all_article:
            result.append(prod)


    ###### поиск по кросам
    for products in all_product:
        all_cross = ProductCross.objects.filter(product=products.product)
        for cross in all_cross:
            if cross.cross == data:
                result.append(products)
    print(result)
    page = request.GET.get('page')
    if data =='':
        paginator = Paginator(result, 16)

        print(page, 'page')
        print(data, 'data')
        try:
            result = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            result = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            result = paginator.page(paginator.num_pages)
        return render(request,
                      'landing/search_sort.html',
                      {'page': page,
                       'result': result})

    else:
        return render(request, 'landing/search.html', locals())

def search_sort(request,sort):
    if sort == '1':
        sorting = '-product__price'
    elif sort == '2':
        sorting = 'product__price'
    result = ProductImage.objects.filter(is_active=True).order_by(sorting)
    page = request.GET.get('page')

    # return render(request, 'landing/search.html', locals())
    paginator = Paginator(result, 16)
    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        result = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        result = paginator.page(paginator.num_pages)
    return render(request,
                  'landing/search_sort.html',
                  {'page': page,
                   'result': result})


def contact(request):
    return render(request, 'landing/contact.html', locals())

