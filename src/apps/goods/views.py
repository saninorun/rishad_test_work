from django.conf import settings
from django.shortcuts import render
from django.views.generic import TemplateView

from apps.goods.models import Product


def product(request, slug):
    product = Product.objects.get(slug=slug)
    context = {
        'title': 'Тестовый магазин',
        "product": product,
        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
    }

    return render(request, "goods/product.html", context=context)


class CatalogView(TemplateView):
    template_name = "goods/catalog.html"
    extra_context = {
        'title': 'Тестовый магазин',
        'goods': Product.objects.all(),
        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
    }
