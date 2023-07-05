from django.urls import path
from rest_framework import routers

from .views import ShopView, CartView, ProductSingleView, CartViewSet, WishlistView, WishlistViewSet, \
    WishlistDeleteView, WishlistAddView

app_name = 'store'

router = routers.DefaultRouter()
router.register(r'cart', CartViewSet)
router.register(r'wishlist', WishlistViewSet)


urlpatterns = [
    path('', ShopView.as_view(), name='shop'),
    path('cart/', CartView.as_view(), name='cart'),
    path('product/<int:id>/', ProductSingleView.as_view(), name='product'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('wishlist/del/<int:id>/', WishlistDeleteView.as_view(), name='wishlistdel'),
    path('wishlist/add/<int:id>/', WishlistAddView.as_view(), name='wishlistadd'),
]
