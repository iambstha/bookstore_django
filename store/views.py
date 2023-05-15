from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import CategoriesForm, ItemsForm, SignupForm
from .models import Categories, Item, RegUser, Cart

def index(req):
    user_id = req.session.get('user_id')
    try:
        user = RegUser.objects.get(pk=user_id)
    except RegUser.DoesNotExist:
        user = None
    return render(req, 'store/index.html', {'user': user})


def addCategory(req):
    user_id = req.session.get('user_id')
    try:
        user = RegUser.objects.get(pk=user_id)
    except RegUser.DoesNotExist:
        user = None
    if req.method == 'POST':
        data = CategoriesForm(req.POST)
        if data.is_valid():
            data.save()
            return redirect('shop')
    else:
        data = CategoriesForm()
    return render(req, 'store/addcategory.html', {'data' : data, 'user' : user})

def addItem(req):
    user_id = req.session.get('user_id')
    try:
        user = RegUser.objects.get(pk=user_id)
    except RegUser.DoesNotExist:
        user = None
    if req.method == 'POST':
        data = ItemsForm(req.POST)
        if data.is_valid():
            data.save()
            return redirect('shop')
    else:
        data = ItemsForm()
    return render(req, 'store/additem.html', {'data' : data, 'user' : user})

def shop(req):
    user_id = req.session.get('user_id')
    try:
        user = RegUser.objects.get(pk=user_id)
    except RegUser.DoesNotExist:
        user = None
    categories = Categories.objects.all()
    items = Item.objects.all()
    return render(req, 'store/shop.html',{
        'categories' : categories,
        'items' : items,
        'user' : user
    })
@csrf_protect
def signup(req):
    user_id = req.session.get('user_id')
    try:
        user = RegUser.objects.get(pk=user_id)
    except RegUser.DoesNotExist:
        user = None
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')
        data = RegUser(username = username, password=password)
        data.set_password(password)
        data.save()
        # login(req, data)
        return redirect('index')
    else:
        data = SignupForm()
    return render(req, 'store/signup.html', {'data' : data, 'user' : user})

@csrf_protect
def signin(request):
    user_id = request.session.get('user_id')
    try:
        user = RegUser.objects.get(pk=user_id)
    except RegUser.DoesNotExist:
        user = None
    data = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = RegUser.objects.get(username=username)
        print(user)
        if user.check_password(password):
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            request.session['user_id'] = user.pk
            return redirect('shop')
        else:
            return redirect('index')
    return render(request, 'store/signin.html',{'data' : data, 'user' : user})

def logout_view(request):
    logout(request)
    return render(request, 'store/index.html', {'message': 'You have been logged out.'})

def logout(request):
    user_id = request.session.clear()
    try:
        user = RegUser.objects.get(pk=user_id)
    except RegUser.DoesNotExist:
        user = None
    return render(request, 'store/logout.html',{'user' : user})

# @login_required
@csrf_protect
def add(request):
    if 'user_id' in request.session:
        if request.method == 'POST':
            item_id = request.POST.get('item_id')
            item = Item.objects.get(id=item_id)
            # user = None
            try:
                user_id = request.session.get('user_id')
                user = RegUser.objects.get(pk=user_id)
            except RegUser.DoesNotExist:
                messages.error(request, f"No user found with ID {user_id}")
                return redirect('shop')
            
            cart_item = Cart.objects.filter(user=user, item=item).first()
            if cart_item is not None:
                cart_item.quantity += 1
                cart_item.save()
            else:
                cart_item = Cart(user=user, item=item)
                cart_item.save()
        else:
            messages.error(request, "Invalid request")
    else:
        messages.error(request, "You must be logged in to add items to cart")
        return redirect('signin')
    return redirect('shop')

def mycart(req):
    user_id = req.session.get('user_id')
    try:
        user = RegUser.objects.get(pk=user_id)
    except RegUser.DoesNotExist:
        user = None
    carts = Cart.objects.filter(user=user).all()
    items = Item.objects.filter(cart__in=carts)
    total = 0
    for cart in carts:
        total = total + cart.item.sell_price * cart.quantity
    print(len(carts))
    return render(req, 'store/mycart.html',{
        'user' : user,
        'items' : items,
        'carts' : carts,
        'total' : total,
        'len' : len(carts)
    })

