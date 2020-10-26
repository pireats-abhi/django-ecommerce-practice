from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from .models import Product, Category, Customer, Order
from .functions import validate_customer, register_user
from django.views import View
from django.urls import reverse


class Index(View):
    def get(self, request, id=0):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        if id == 0:
            products = Product.get_all_product()
            categories = Category.get_all_categories()
        else:
            categories = Category.get_all_categories()
            products = Product.get_all_product_by_category_id(id)

        data = {}
        data['products'] = products
        data['categories'] = categories
        data['active'] = id
        return render(request, 'store/index.html', data)
    def post(self, request, id=0):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        if id == 0:
            return redirect('store:index')
        else:
            return redirect('store:category_index', id=id)


class SignUp(View):
    def get(self, request):
        return render(request, 'store/signup.html')
    def post(self, request):
        return register_user(request)


class Login(View):
    return_url = None
    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        print(Login.return_url)
        return render(request, 'store/login.html')
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('store:index')
            else:
                error_message = "Wrong password"
        else:
            error_message = "Invalid Email"
        return render(request, 'store/login.html', {'error': error_message})


class Logout(View):
    def get(self, request):
        request.session.clear()
        return redirect('store:index')


class Cart(View):
    def get(self, request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        return render(request, 'store/cart.html', {'products': products})


class CheckOut(View):
    def get(self, request):
        return redirect('store:cart')

    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))

        for product in products:
            order = Order(customer = Customer(id = customer), product = product, address = address, phone = phone, price = product.price, quantity = cart.get(str(product.id)))

            order.place_order()

        request.session['cart'] = {}

        return redirect('store:cart')


class OrderView(View):

    def get(self, request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        return render(request, 'store/orders.html', {'orders': orders})