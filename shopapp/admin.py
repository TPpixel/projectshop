from django.contrib import admin
from django.contrib import admin
from .models import Category, Manufacturer, Product, Basket, BasketItem


admin.site.register(Category)
admin.site.register(Manufacturer)
admin.site.register(Product)
admin.site.register(Basket)
admin.site.register(BasketItem)