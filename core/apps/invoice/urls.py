from django.urls import path, re_path

from .views import requestInvoice

urlpatterns = [
    path('request-invoice/', requestInvoice.as_view(), name='request-invoice'),
    
]