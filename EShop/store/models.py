from django.db import models
import datetime


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    @staticmethod
    def get_all_categories():
        return Category.objects.all()


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='uploads/products/')

    def __str__(self):
        return self.name

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in = ids)

    @staticmethod
    def get_all_product():
        return Product.objects.all()

    @staticmethod
    def get_all_product_by_category_id(category_id):
        if category_id:
            return Product.objects.filter(category = category_id)
        else:
            return Product.get_all_product()


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=500)

    def register(self):
        self.save()

    def isExist(self):
        if Customer.objects.filter(email = self.email):
            return True
        else:
            return False

    def __str__(self):
        return (f'{self.first_name} {self.last_name}')

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email = email)
        except Customer.DoesNotExist:
            return False


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def place_order(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer = customer_id).order_by('-date')

