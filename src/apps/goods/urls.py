from django.urls import path
from apps.goods.views import CatalogView, product


app_name = 'goods'

urlpatterns = [
    path('', CatalogView.as_view(), name='index'),
    path('product/<slug:slug>/', product, name='product'),
]