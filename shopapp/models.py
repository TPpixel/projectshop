from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Category(models.Model):
    название = models.CharField(max_length=100)
    #описание = models.TextField(blank=True)

    def __str__(self):
        return self.название


class Manufacturer(models.Model):
    название = models.CharField(max_length=100)
    страна = models.CharField(max_length=100)
    #описание = models.TextField(blank=True)

    def __str__(self):
        return self.название


class Product(models.Model):
    название = models.CharField(max_length=200)
    описание = models.TextField()
    фото_товара = models.ImageField(upload_to='products/')
    цена = models.DecimalField(max_digits=10, decimal_places=2)
    количество_на_складе = models.IntegerField()
    категория = models.ForeignKey(Category, on_delete=models.CASCADE)
    производитель = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)

    def __str__(self):
        return self.название

    def clean(self):
        if self.цена < 0:
            raise ValidationError("Цена не может быть отрицательной")

        if self.количество_на_складе < 0:
            raise ValidationError("Количество на складе не может быть отрицательным")


class Basket(models.Model):
    пользователь = models.OneToOneField(User, on_delete=models.CASCADE)
    дата_создания = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Корзина пользователя {self.пользователь.username}"

    def общая_стоимость(self):
        items = self.basketitem_set.all()
        total = sum(item.стоимость_элемента() for item in items)
        return total


class BasketItem(models.Model):
    корзина = models.ForeignKey(Basket, on_delete=models.CASCADE)
    товар = models.ForeignKey(Product, on_delete=models.CASCADE)
    количество = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.товар.название} ({self.количество} шт.)"

    def стоимость_элемента(self):
        return self.товар.цена * self.количество

    def clean(self):
        if self.количество > self.товар.количество_на_складе:
            raise ValidationError("Количество превышает остаток на складе")