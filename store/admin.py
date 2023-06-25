from django.contrib import admin

from store.models import Category, Product, Discount

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Discount)
