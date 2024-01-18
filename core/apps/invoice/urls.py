from django.urls import path
from .views import requestInvoice, fetchInvoiceItems

urlpatterns = [
    path('request-invoice/', requestInvoice.as_view(), name='request-invoice'),
    path('fetch-invoice-items/', fetchInvoiceItems.as_view(), name='fetch-invoice-items'),
]