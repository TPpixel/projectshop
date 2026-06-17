from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'api/categories', views.CategoryViewSet)
router.register(r'api/manufacturers', views.ManufacturerViewSet)
router.register(r'api/products', views.ProductViewSet)
router.register(r'api/baskets', views.BasketViewSet)
router.register(r'api/basket-items', views.BasketItemViewSet)
router.register(r'api/orders', views.OrderViewSet)
router.register(r'api/order-items', views.OrderItemViewSet)

urlpatterns = [
    path('', views.hello_world, name='hello_world'),
    path('catalog/', views.product_list, name='product_list'),
    path('catalog/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('checkout/', views.checkout, name='checkout'),
] + router.urls
