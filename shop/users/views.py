from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from orders import views
from django.contrib.auth import authenticate
from orders.models import *
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth import views
from django.urls import reverse
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
from utils.emails import SendingEmail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random

class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "landing/login.html"
    success_url = "/"

    def form_valid(self, form):

        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)

class LoginFormViewBasket(FormView):
    form_class = AuthenticationForm
    template_name = "landing/login.html"
    success_url = "/checkout/"

    def form_valid(self, form):

        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormViewBasket, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")


def register(request):
    if request.method == 'POST':
        data = request.POST
        email_user = data.get('email')
        print(email_user)
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            passwords = user_form.cleaned_data['password']
            email = SendingEmail()
            email.sending_email(type_id=3, email=email_user,password=passwords)

            return render(request, 'landing/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'landing/register.html', {'user_form': user_form})


def login_in_basket(request):
    data = request.POST
    session = data.get('session')
    user_name = data.get('username')
    password = data.get('password')
    user = authenticate(username=user_name, password=password)
    print(data)
    return render(request, 'orders/checkout.html', locals())


def lk(request):
    user_name = request.user
    user, created = User.objects.get_or_create(username=user_name)
    order_history = Order.objects.filter(customer_name=user).order_by("-created")
    paginator = Paginator(order_history,5)
    page = request.GET.get('page')
    print(type(page))
    try:
        order_history = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        order_history = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        order_history = paginator.page(paginator.num_pages)
    print(page)

    return render(request,
                  'LK/lk.html',
                  {'page': page,
                   'order_history': order_history})


def lk_order(request,order_id):
    order_lk = Order.objects.filter(id=order_id)
    basket_order = ProductInOrder.objects.filter(order=order_lk)
    total_price = order_lk[0].total_price
    ship = order_lk[0].ship_metod
    order = order_lk[0]
    return render(request, 'LK/lk_order.html', locals())

def password_change(request,
                    template_name='LK/lk.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    extra_context=None):
    data= request.POST
    passwords = data.get('new_password1')
    user_email = request.user.email
    print(user_email,'dfwefewfewfwefwef')
    if post_change_redirect is None:
        post_change_redirect = reverse('password_change_done')
    else:
        post_change_redirect = resolve_url(post_change_redirect)
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Updating the password logs out all other sessions for the user
            # except the current one.
            update_session_auth_hash(request, form.user)
            email = SendingEmail()
            email.sending_email(type_id=4, email=user_email, password=passwords)
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
        'title': _('Password change'),
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


def password_change_done(request,
                         template_name='lk/password_change_done.html',
                         extra_context=None):
    context = {
        'title': ('Password change successful'),
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name)


def reset_password(request):
    return render(request, 'lk/reset.html', locals())


def reset_password_done(request):
    data = request.POST
    email_user = data.get('email')
    users = User.objects.filter(email=email_user)

    if users:
        print(users,'users')
        user = User.objects.get(email=email_user)
        psw = ''
        for x in range(12):
            psw = psw + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'))
        username = user.username
        user.set_password(psw)
        user.save()
        email = SendingEmail()
        email.sending_email(type_id=5, email=email_user, password=psw)
        logout(request)

        # return HttpResponseRedirect(request, 'lk/reset_done.html', locals())
    return render(request, 'lk/reset_done.html', locals())