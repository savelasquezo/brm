from django.urls import path, re_path
import apps.item.views as view


urlpatterns = [
    path('fetch-items/', view.fetchItems.as_view(), name='fetch-items'),
]