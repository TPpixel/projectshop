from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product, Category, Manufacturer, Basket, BasketItem


def hello_world(request):
    return render(request, 'index.html')


def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    manufacturers = Manufacturer.objects.all()

    category_id = request.GET.get('category')
    manufacturer_id = request.GET.get('manufacturer')
    query = request.GET.get('q')

    if category_id:
        products = products.filter(категория_id=category_id)
    if manufacturer_id:
        products = products.filter(производитель_id=manufacturer_id)
    if query:
        products = products.filter(
            Q(название__icontains=query) | Q(описание__icontains=query)
        )

    return render(request, 'shop/product_list.html', {
        'products': products,
        'categories': categories,
        'manufacturers': manufacturers,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    basket, _ = Basket.objects.get_or_create(пользователь=request.user)
    item, created = BasketItem.objects.get_or_create(
        корзина=basket,
        товар=product,
        defaults={'количество': 1}
    )
    if not created and item.количество < product.количество_на_складе:
        item.количество += 1
        item.save()
    return redirect('cart_view')


@login_required
def update_cart(request, item_id):
    item = get_object_or_404(BasketItem, pk=item_id, корзина__пользователь=request.user)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if 0 < quantity <= item.товар.количество_на_складе:
            item.количество = quantity
            item.save()
    return redirect('cart_view')


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(BasketItem, pk=item_id, корзина__пользователь=request.user)
    if request.method == 'POST':
        item.delete()
    return redirect('cart_view')


@login_required
def cart_view(request):
    basket, _ = Basket.objects.get_or_create(пользователь=request.user)
    items = basket.basketitem_set.all()
    return render(request, 'shop/cart.html', {
        'basket': basket,
        'items': items,
        'total': basket.общая_стоимость(),
    })
