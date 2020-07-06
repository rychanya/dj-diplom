from django.contrib import admin

from .models import Product, Compilation, Category, CategoryHub, Review, CartIteam, Cart, Order, OrderIteam
# Register your models here.

class OrderIteamInLine(admin.TabularInline):
    model = OrderIteam
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderIteamInLine, )

class CartIteamInLine(admin.TabularInline):
    model = CartIteam
    extra = 1

class CartAdmin(admin.ModelAdmin):
    inlines = (CartIteamInLine, )

admin.site.register(Product)
admin.site.register(Compilation)
admin.site.register(Category)
admin.site.register(CategoryHub)
admin.site.register(Review)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)


