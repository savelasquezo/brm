from django.urls import path
import apps.user.views as view

urlpatterns = [
    path('add-item-shopcart/', view.addItemShopcart.as_view(), name='add-item-shopcart'),
    path('fetch-shopcart/', view.fetchShopCart.as_view(), name='fetch-shopcart'),
]