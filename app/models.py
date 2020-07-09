from django.contrib.auth.models import User
from django.db import models


class BaseMenuIteam(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")

    def __str__(self):
        if hasattr(self, "categoryhub"):
            return f"Группа {self.name}"
        return self.name


class Category(BaseMenuIteam):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class CategoryHub(BaseMenuIteam):
    items = models.ManyToManyField(Category, verbose_name="Содержимое")

    class Meta:
        verbose_name = "Группа меню"
        verbose_name_plural = "Группы меню"


class Menu(models.Model):
    content = models.OneToOneField(
        BaseMenuIteam, on_delete=models.CASCADE, verbose_name="Содержимое"
    )
    index = models.IntegerField(default=0, verbose_name="Порядковый номер")

    def __str__(self):
        return str(self.content)

    class Meta:
        ordering = ["index"]
        verbose_name = "Пункт меню"
        verbose_name_plural = "Меню"


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    image = models.ImageField(upload_to="img", verbose_name="Изображение")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Категория",
    )
    text = models.TextField(verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Cart(models.Model):
    products = models.ManyToManyField(Product, through="CartIteam")
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Корзина {self.user}"

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"


class CartIteam(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="carter"
    )
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)

    @classmethod
    def get_sum_count(cls, cart):
        return cls.objects.filter(cart=cart).aggregate(models.Sum("count"))[
            "count__sum"
        ]


class Compilation(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    text = models.CharField(max_length=100, verbose_name="Текст")
    products = models.ManyToManyField(Product, verbose_name="Товары")
    create_date = models.DateTimeField(auto_now=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Подборка"
        verbose_name_plural = "Подборки"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    user = models.CharField(max_length=100, verbose_name="Кто оставил")
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.IntegerField(verbose_name="Рейтинг")

    def __str__(self):
        return f"обзор на {self.product} от {self.user}"

    class Meta:
        verbose_name = "Обзор"
        verbose_name_plural = "Обзоры"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Заказчик")
    products = models.ManyToManyField(
        Product, through="OrderIteam", verbose_name="Списко продуктов"
    )
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderIteam(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="ordering"
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
