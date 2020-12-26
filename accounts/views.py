from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .decorators import unauthenticated_user
from .models import *
from .forms import OrderForm, CustomerForm, CreateUserForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from .decorators import unauthenticated_user
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='login')
def dashboard(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    totalorder = orders.count()
    orderpending = orders.filter(status="pending").count()
    orderdelivered = orders.filter(status="delivered").count()
    outfordelivery = orders.filter(status="out for delivery").count()
    context = {
        'customers': customers,
        'orders': orders,
        "totalorder": totalorder,
        'orderpending': orderpending,
        'orderdelivered': orderdelivered,
        'outfordelivery': outfordelivery,
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
def customer(request, pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()
    ordercount = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {
        'myFilter': myFilter,
        'customer': customer,
        'orders': orders,
        'ordercount': ordercount,
    }
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
def product(request):
    products = Product.objects.all()
    return render(request, 'accounts/product.html', {'products': products})


@login_required(login_url='login')
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status', 'note'), extra=8)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # forms = OrderForm(initial={"customer": customer})
    if request.method == 'POST':
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect("/")
    context = {"formset": formset, "customer": customer}
    return render(request, 'accounts/create_form.html', context)


@login_required(login_url='login')
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    forms = OrderForm(instance=order)

    if request.method == "POST":
        forms = OrderForm(request.POST, instance=order)

        if forms.is_valid():
            forms.save()
            return redirect("/")

    context = {"forms": forms}
    return render(request, 'accounts/update_form.html', context)


@login_required(login_url='login')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    context = {"order": order}
    if request.method == 'POST':
        order.delete()
        return redirect('home')
    return render(request, 'accounts/delete.html', context)


@login_required(login_url='login')
def createCustomer(request):
    forms = CustomerForm()
    # forms = OrderForm(initial={"customer": customer})
    if request.method == 'POST':
        forms = CustomerForm(request.POST)
        if forms.is_valid():
            nm = forms.cleaned_data['name']
            eml = forms.cleaned_data['email']
            phn = forms.cleaned_data['phone']

            obj = Customer(name=nm, email=eml, phone=phn)
            obj.save()
            return redirect("/")
    context = {"forms": forms}
    return render(request, 'accounts/create_customer.html', context)


@login_required(login_url='login')
def deleteCustomer(request, pk):
    customer = Customer.objects.get(id=pk)

    if request.method == 'POST':
        customer.delete()
        return redirect('home')

    context = {"customer": customer}
    return render(request, 'accounts/delete.html', context)


@login_required(login_url='login')
def updateCustomer(request):
    context = {}
    return render(request, 'accounts/create_customer.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        return redirect('home')
    else:
        messages.error(request, 'Username or Password wrong !!')

    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect("login")

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data['username']
            messages.info(request, 'you are registered as' + " " + user + "!!")
            return redirect("login")

    context = {'form': form}
    return render(request, 'accounts/register.html', context)

def userPage(request):
    context = {}
    return render(request, 'accounts/user.html', context)
