from django.urls import path

from other.views import CurrentDateView, HelloWorld, IndexView, RandomNumber

# from .views import CurrentDateView, HelloWorld, RandomNumber, IndexView

urlpatterns = [
    path('', IndexView.as_view()),
    path('datetime/', CurrentDateView.as_view()),
    path('hello/', HelloWorld.as_view()),
    path('random/', RandomNumber.as_view()),
]
