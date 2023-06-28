from django.urls import path
from rest_framework import routers

from .views import ShopView, CartView, ProductSingleView, CartViewSet


app_name = 'store'

router = routers.DefaultRouter()
router.register(r'cart', CartViewSet)


urlpatterns = [
    path('', ShopView.as_view(), name='shop'),
    path('cart/', CartView.as_view(), name='cart'),
    path('product/<int:id>/', ProductSingleView.as_view(), name='product'),

]
