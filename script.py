import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from store.models import Product, Category


if __name__ == '__main__':

    category = Category.objects.get(name='Vegetables')
    obj = Product(name='Carrots', description='Carrots', price=120,
                  image='static/products/product-7.jpg',
                  category=category)
    obj.save()

    obj = Product.objects.create(name='Fruit Juice',
                                 description='Juice',
                                 price=120,
                                 image='static/products/product-8.jpg',
                                 category=Category.objects.get(name='Juice'))

    data = [{'name': 'Onion',
             'price': 120.00,
             'description': 'Onion',
             'image': 'static/products/product-9.jpg',
             'category': 'Vegetables'},
            {'name': 'Apple',
             'price': 120.00,
             'description': 'Iphone',
             'image': 'static/products/product-10.jpg',
             'category': 'Fruits'},
            ]

    categor = {'Fruits': Category.objects.get(name='Fruits'),
               'Vegetables': Category.objects.get(name='Vegetables'),
               }
    objects_to_create = [Product(name=val1['name'],
                                 description=val1['description'],
                                 price=val1['price'],
                                 image=val1['image'],
                                 category=categor[val1['category']]) for val1 in data]
    Product.objects.bulk_create(objects_to_create)
