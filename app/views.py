from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Product, Compilation, Category, get_meny, Review, Cart, CartIteam
from .forms import LoginForm

# Create your views here.


def home(request):
    return render(
        request,
        'app/index.html',
        context={
            'products': Product.objects.all(),
            'compilations': Compilation.objects.order_by('-create_date').prefetch_related('products').all(),
            'meny_iteams': get_meny(),
        }
    )

def product(request, id=None):
    product = get_object_or_404(Product, pk=id)
    reviews = Review.objects.filter(product=product).all()
    return render(
        request,
        'app/product_detail.html',
        context={
            'product': product,
            'meny_iteams': get_meny(),
            'reviews': reviews,
            'stars': list(range(1,6)),
        }
    )

def category_view(request):
    category = get_object_or_404(Category, pk=request.GET.get('category'))
    products = Product.objects.filter(category=category).all()

    paginator = Paginator(products, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if page_obj.has_previous():
        skip_left = page_obj.number > 2
    else:
        skip_left = False

    if page_obj.has_next():
        skip_right = (paginator.num_pages - page_obj.number) > 1
    else:
        skip_right = False

    return render(
        request,
        'app/category.html',
        context={
            'category': category,
            'products': page_obj,
            'skip_left': skip_left,
            'skip_right': skip_right,
            'meny_iteams': get_meny(),
        }
    )

@login_required
def cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart_iteams = CartIteam.objects.select_related('product').filter(cart=cart).all()
        count = CartIteam.get_sum_count(cart)
    else:
        cart_iteams = []
        count = 0
    return render(
        request,
        'app/cart.html',
        context={
            'cart_iteams': cart_iteams,
            'count': count,
            'meny_iteams': get_meny(),
        }
    )

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        next_page = form['next'].data or '/'
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password) or\
                authenticate(request, email=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(form.cleaned_data.get('next', '/'))
            else:
                form.add_error(None, 'Имя, почта или пароль неправильные')
    else:
        form = LoginForm()
        next_page = request.GET.get('next') or '/'
    return render(
        request,
        'app/login.html',
        context={
            'form': form,
            'box_center': 'text-center',
            'next': next_page
        }
    )

def logout_view(request):
    logout(request)
    return redirect('home')
