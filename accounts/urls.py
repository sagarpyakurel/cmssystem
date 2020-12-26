from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="home"),
    path('product', views.product, name="product"),
    path('customer/<str:pk>/', views.customer, name="customer"),
    path('create_order/<str:pk>/', views.createOrder, name='create_order'),
    path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>/', views.deleteOrder, name='delete_order'),
    path('createcustomer', views.createCustomer, name='create_customer'),
    path('delete_customer/<str:pk>/', views.deleteCustomer, name='delete_customer'),
    path('user/',views.userPage,name='user-page'),

    path('login', views.loginPage, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('register', views.registerPage, name='register'),
]
