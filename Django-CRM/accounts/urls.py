from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginpage, name= "login"),
    path('logout/', views.logoutpage, name= "logout"),
    path('registration/', views.registration, name= "registration"),
    path('user/', views.user, name="user"),
    path('', views.home, name = "home"),
    path('product/', views.product, name = "product"),
    path('customer/<str:pk_test>', views.customer, name="customer"),
    path('create_order/<str:pk>', views.createOrder, name="createupdate"),
    path('update_order/<str:pk>', views.updateOrder, name="updateorder"),
    path('delete_order/<str:pk>', views.deleteOrder, name="deleteorder")
]
