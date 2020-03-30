from django.contrib import admin

# Register your models here.c
#from .models import Customer
from .models import Product, Customer, Order, Tag
#from .models import Order

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Tag)