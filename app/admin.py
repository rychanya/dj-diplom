from django.contrib import admin
from django.db import models

from .models import (
    Cart,
    CartIteam,
    Category,
    CategoryHub,
    Compilation,
    Menu,
    Order,
    OrderIteam,
    Product,
    Review,
)

# Register your models here.


class OrderIteamInLine(admin.TabularInline):
    model = OrderIteam
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    def sum_by_cart(self, obj):
        return OrderIteam.objects.filter(order=obj).aggregate(models.Sum("count"))[
            "count__sum"
        ]

    inlines = (OrderIteamInLine,)
    list_display = ("id", "user", "created_date", "sum_by_cart")
    ordering = ["-created_date"]


class CartIteamInLine(admin.TabularInline):
    model = CartIteam
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = (CartIteamInLine,)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    def product_name(self, obj):
        return obj.product.name

    list_display = ("id", "product_name", "user", "rating")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category")


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("__str__", "index")
    list_editable = ("index",)


admin.site.register(Compilation)
admin.site.register(Category)
admin.site.register(CategoryHub)
# admin.site.register(Menu)
