from django.contrib import admin

from .models import Product, Compilation, Category, CategoryHub, Review, CartIteam, Cart
# Register your models here.

admin.site.register(Product)
admin.site.register(Compilation)
admin.site.register(Category)
admin.site.register(CategoryHub)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(CartIteam)

