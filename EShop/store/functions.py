from .models import Customer
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import redirect, render


def validate_customer(customer):
    error_message = None

    if not customer.first_name:
        error_message = 'First name required!!!'
    elif len(customer.first_name) > 50:
        error_message = 'Invalid First name!!!'
    elif not customer.last_name:
        error_message = 'Last name required!!!'
    elif len(customer.last_name) > 50:
        error_message = 'Invalid Last name!!!'
    elif not customer.phone:
        error_message = 'Phone Number required!!!'
    elif len(customer.phone) < 10 or len(customer.phone) > 15:
        error_message = 'Invalid Phone Number!!!'
    elif len(customer.password) < 8:
        error_message = 'Password must be at least 8 character!!!'
    elif customer.isExist():
        error_message = 'Email already registered!!!'

    return error_message


def register_user(request):
    post_data = request.POST
    first_name = post_data.get('firstname')
    last_name = post_data.get('lastname')
    phone = post_data.get('phone')
    email = post_data.get('email')
    password = post_data.get('password')

    value = {
        'first_name': first_name,
        'last_name': last_name,
        'phone': phone,
        'email': email
    }

    customer = Customer(first_name=first_name, last_name=last_name, phone=phone, email=email, password=password)

    error_message = validate_customer(customer)

    if not error_message:
        customer.password = make_password(customer.password)
        customer.register()
        return redirect('store:index')
    else:
        data = {
            'error': error_message,
            'values': value
        }
        return render(request, 'store/signup.html', data)
            