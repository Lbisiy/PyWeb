from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.db.models import OuterRef, Subquery, F, ExpressionWrapper, DecimalField, Case, When
from django.utils import timezone

from store.models import Product, Discount, Cart, Wishlist
from rest_framework import viewsets, response
from rest_framework.permissions import IsAuthenticated
from .serializers import CartSerializer, WishlistSerializer
from django.shortcuts import get_object_or_404


class WishlistAddView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            if Wishlist.objects.filter(product_id=id):
                return redirect('store:shop')
            else:
                Wishlist.objects.create(user=request.user, product_id=id)
                return redirect('store:shop')
        else:
            return redirect('login:login')


class WishlistView(View):
    def get(self, request):
        if request.user.is_authenticated:
            data = Wishlist.objects.filter(user=request.user)
           # код который необходим для обработчика
            return render(request, "store/wishlist.html", {'data': data})
       # Иначе отправляет авторизироваться
        return redirect('login:login')  # from django.shortcuts import redirect


class WishlistDeleteView(View):
    def get(self, request, id):
        Wishlist.objects.filter(user=request.user, id=id).delete()
        data = Wishlist.objects.filter(user=request.user)
       # return render(request, "store/wishlist.html", {'data': data})
        return redirect('store:wishlist')


class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        cart_items = self.get_queryset().filter(product__id=request.data.get('product'))

        if cart_items:
            cart_item = cart_items[0]
            if request.data.get('quantity'):
                cart_item.quantity += int(request.data.get('quantity'))
            else:
                cart_item.quantity += 1
        else:
            product = get_object_or_404(Product, id=request.data.get('product'))
            if request.data.get('quantity'):
                cart_item = Cart(user=request.user, product=product, quantity=request.data.get('quantity'))
            else:
                cart_item = Cart(user=request.user, product=product)

        cart_item.save()
        return response.Response({'message': 'Product added to cart'}, status=201)

    def update(self, request, *args, **kwargs):
        cart_item = get_object_or_404(Cart, id=kwargs['pk'])

        if request.data.get('quantity'):
            cart_item.quantity = request.data['quantity']
        if request.data.get('product'):
            product = get_object_or_404(Product, id=request.data['product'])
            cart_item.product = product

        cart_item.save()
        return response.Response({'message': 'Product change to cart'}, status=201)

    def destroy(self, request, *args, **kwargs):
        cart_item = self.get_queryset().get(id=kwargs['pk'])

        cart_item.delete()
        return response.Response({'message': 'Product delete from cart'}, status=201)


class ShopView(View):

    def get(self, request):

        discount_value = Case(When(discount__value__gte=0,
                                   discount__date_begin__lte=timezone.now(),
                                   discount__date_end__gte=timezone.now(),
                                   then=F('discount__value')),
                              default=0,
                              output_field=DecimalField(max_digits=10,
                                                        decimal_places=2)
                              )
        price_with_discount = ExpressionWrapper(
            F('price') * (100.0 - F('discount_value')) / 100.0,
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )

        products = Product.objects.annotate(discount_value=discount_value,
                                            price_before=F('price'),
                                            price_after=price_with_discount
                                            ).values('id', 'name', 'image', 'price_before', 'price_after',
                                                     'discount_value')

        return render(request, 'store/shop.html', {'data': products})


class CartView(View):
    def get(self, request):
        return render(request, 'store/cart.html')


class ProductSingleView(View):

    def get(self, request, id):
        data = Product.objects.get(id=id)
        return render(request, 'store/product-single.html',
                      context={'name': data.name,
                               'description': data.description,
                               'price': data.price,
                               'rating': 5.0,
                               'url': data.image.url,
                               })

        # return render(request, 'store/product-single.html', context=data[id])
