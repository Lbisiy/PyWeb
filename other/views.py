from django.shortcuts import render

# Create your views here.

from datetime import datetime
from django.views import View
from django.http import HttpResponse
from random import random

random_number = random()


class IndexView(View):
    def get(self, request):
        return render(request, 'other/index.html')


class CurrentDateView(View):
    def get(self, request):
        html = f'<h3>{datetime.now()}</h3>'
        return HttpResponse(html)


class RandomNumber(View):
    def get(self, request):
        html = f'<h1>{random_number}<h1>'
        return HttpResponse(html)


class HelloWorld(View):
    def get(self, request):
        html = '<h1>Hello, World</h1>'
        return HttpResponse(html)
