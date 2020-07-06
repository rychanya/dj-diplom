from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from itertools import chain

class Category(models.Model):
    name = models.CharField(max_length=100)
    solo = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    menu_index = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    

class CategoryHub(models.Model):
    name = models.CharField(max_length=100)
    items = models.ManyToManyField(Category)
    active = models.BooleanField(default=True)
    menu_index = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    

def get_meny():
    solo_category = Category.objects.filter(solo=True, active=True).all()
    hubs = CategoryHub.objects.filter(active=True).all()
    return sorted(
        chain(solo_category, hubs),
        key=lambda iteam: iteam.menu_index
    )

class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='img')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField()

    def __str__(self):
        return self.name
    

class Cart(models.Model):
    products = models.ManyToManyField(Product, through='CartIteam')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Корзина {self.user}'
    

class CartIteam(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='carter')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    @classmethod
    def get_sum_count(cls, cart):
        return cls.objects.filter(cart=cart).aggregate(models.Sum('count'))['count__sum']

class Compilation(models.Model):
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=100)
    products = models.ManyToManyField(Product)
    create_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    text = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f'обзор на {self.product} от {self.user}'
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderIteam')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Заказ #{self.id} от {self.user}'
    

class OrderIteam(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ordering')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)