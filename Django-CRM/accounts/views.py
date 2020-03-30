from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm
from .filter import OrderFilter
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group

# Create your views here.

@unauthenticated_user
def loginpage(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    # else:
    if request.method== "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'UserName Or Password is Inccorect !!!')
                return redirect('login')
    context ={}
    return render(request, 'accounts/login.html', context)

@unauthenticated_user
def registration(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    # else:
    if request.method =="POST":
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')

                group = Group.objects.get(name='customer')
                user.groups.add(group)

                messages.success(request,'Account was create for '+user)
                return redirect('login')
    form = RegistrationForm()
    context = {'form':form}
    return render(request, 'accounts/registration.html', context)

def logoutpage(request):
    logout(request)
    return redirect('login')

def user(request):
    context = {}
    return render(request, 'accounts/user.html', context)


@admin_only
# @allowed_users(allowed_roles =['admin'])
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_order = orders.count()
    total_pending = orders.filter(status = 'Pending').count()
    delivered = orders.filter(status = 'Delivered').count()

    context= {'orders': orders, 'customers': customers, 'total_order': total_order,
    'total_pending': total_pending, 'delivered': delivered}

    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
def product(request): 
    product = Product.objects.all()
    return render(request, 'accounts/product.html', {'product':product})

@login_required(login_url='login')
def customer(request, pk_test): 
    customer = Customer.objects.get(id = pk_test)
    orders = customer.order_set.all()
    total_order = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context={'customer':customer, 'orders': orders, 'total_order':total_order, 'myFilter':myFilter}
    return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
def createOrder(request, pk):
    OrderCreateSet = inlineformset_factory(Customer, Order, fields=('product','status'), extra=-1)
    
    customer = Customer.objects.get(id=pk)
    # form = OrderForm(initial = {'customer':customer})
    formSet = OrderCreateSet(instance = customer)
    context = {'form': formSet}

    if request.method == "POST":
        # form = OrderForm(request.POST)
        formSet = OrderCreateSet(request.POST, instance = customer)
        if formSet.is_valid():
            formSet.save()
            return redirect('home')
    return render(request, 'accounts/createupdate.html', context)

@login_required(login_url='login')
def updateOrder(request, pk):
    order = Order.objects.get(id = pk)
    form = OrderForm(instance=order)
    context = {'form': form}

    if request.method=="POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'accounts/createupdate.html', context)

@login_required(login_url='login')
def deleteOrder(request, pk):
    order = Order.objects.get(id = pk)
    context = {"item":order}
    if request.method=="POST":
        order.delete()
        return redirect('home')
    return render(request, 'accounts/delete.html', context)
