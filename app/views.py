from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AddToCartForm, LoginForm, OderForm, ReviewForm, SigInUpForm
from .models import (
    Cart,
    CartIteam,
    Category,
    Compilation,
    Menu,
    Order,
    OrderIteam,
    Product,
    Review,
)


def home(request):
    return render(
        request,
        "app/index.html",
        context={
            "compilations": Compilation.objects.order_by("-create_date")
            .prefetch_related("products")
            .all(),
        },
    )


def product(request, id=None):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            product = Product.objects.filter(pk=form.cleaned_data["product"]).first()
            if product is not None:
                Review.objects.create(
                    product=product,
                    user=form.cleaned_data["user"],
                    text=form.cleaned_data["text"],
                    rating=form.cleaned_data["rating"],
                )
            return redirect("product-detail", product.id)
    product = get_object_or_404(Product, pk=id)
    reviews = Review.objects.filter(product=product).all()
    form = ReviewForm()
    return render(
        request,
        "app/product_detail.html",
        context={
            "product": product,
            "reviews": reviews,
            "stars": list(range(1, 6)),
            "form": form,
        },
    )


def category_view(request):
    category = get_object_or_404(Category, pk=request.GET.get("category"))
    products = Product.objects.filter(category=category).all()

    paginator = Paginator(products, 3)
    page_number = request.GET.get("page")
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
        "app/category.html",
        context={
            "category": category,
            "products": page_obj,
            "skip_left": skip_left,
            "skip_right": skip_right,
        },
    )


@login_required
def cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    add_message = None
    if request.method == "POST":
        form = AddToCartForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            product_id = form.cleaned_data["product_id"]
            product = Product.objects.filter(pk=product_id).first()
            if product is not None:
                cart_item, _ = CartIteam.objects.get_or_create(
                    product=product, cart=cart, defaults={"count": 0}
                )
                cart_item.count += 1
                cart_item.save()
                add_message = {
                    "msg": f"Товар {product.name} добавлен в корзину.",
                    "valid": True,
                }
            else:
                add_message = {
                    "msg": "Товар не добавлен в корзину.Товара нет в базе.",
                    "valid": False,
                }
        else:
            add_message = {
                "msg": "Товар не добавлен в корзину. ID товара невалидный.",
                "valid": False,
            }

    cart_iteams = CartIteam.objects.select_related("product").filter(cart=cart).all()
    count = CartIteam.get_sum_count(cart)

    return render(
        request,
        "app/cart.html",
        context={
            "cart_iteams": cart_iteams,
            "count": count,
            "add_message": add_message,
            "cart_id": cart.id,
        },
    )


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        next_page = form["next"].data or "/"
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(
                request, username=username, password=password
            ) or authenticate(request, email=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(form.cleaned_data.get("next", "/"))
            else:
                form.add_error(None, "Имя, почта или пароль неправильные")
    else:
        form = LoginForm()
        next_page = request.GET.get("next") or "/"
    return render(
        request,
        "app/login.html",
        context={"form": form, "box_center": "text-center", "next": next_page},
    )


def logout_view(request):
    logout(request)
    return redirect("home")


def siginup_view(request):
    if request.method == "POST":
        form = SigInUpForm(request.POST)
        next_page = form["next"].data or "/"
        if form.is_valid():
            print(")))))")
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            if (
                User.objects.filter(username=username).exists()
                or User.objects.filter(email=email).exists()
            ):
                form.add_error(None, "Имя или почта уже заняты.")
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password
                )
                login(request, user, backend="app.backends.EmailBackend")
                return redirect(form.cleaned_data.get("next", "/"))
    else:
        form = SigInUpForm()
        next_page = request.GET.get("next") or "/"
    return render(
        request,
        "app/siginup.html",
        context={"form": form, "box_center": "text-center", "next": next_page},
    )


@login_required
def order_view(requeest):
    if requeest.method == "POST":
        form = OderForm(requeest.POST)
        if form.is_valid():
            cart_id = form.cleaned_data["cart_id"]
            cart = Cart.objects.filter(pk=cart_id).first()
            if cart is not None and cart.user == requeest.user:
                order = Order.objects.create(user=cart.user)
                for iteam in (
                    CartIteam.objects.select_related("product").filter(cart=cart).all()
                ):
                    OrderIteam.objects.create(
                        product=iteam.product, count=iteam.count, order=order
                    )
                cart.delete()

    return redirect("cart")
