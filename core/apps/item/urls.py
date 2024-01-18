from django.urls import path
from .views import fetchItems

urlpatterns = [
    path('fetch-items/', fetchItems.as_view(), name='fetch-items'),
]