from django.contrib import admin

from store.models import Category, Product, Discount, Cart, Profile

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Discount)
admin.site.register(Cart)
admin.site.register(Profile)
