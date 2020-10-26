from django.urls import path
from . import views
from .auth import auth_middleware


app_name = 'store'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('category/<int:id>/', views.Index.as_view(), name='category_index'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('orders/login/', views.Login.as_view(), name='log_in'),
    path('checkout/login/', views.Login.as_view(), name='check_in'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('cart/', views.Cart.as_view(), name='cart'),
    path('checkout/', auth_middleware(views.CheckOut.as_view()), name='checkout'),
    path('orders/', auth_middleware(views.OrderView.as_view()), name='orders')
]