from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.db.models import OuterRef, Subquery, F, ExpressionWrapper, DecimalField, Case, When
from django.utils import timezone

from store.models import Product


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

        return render(request, 'store/product-single.html', context=data[id])