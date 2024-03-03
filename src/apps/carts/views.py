from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods

from apps.carts.models import Cart
from apps.carts.utils import get_user_carts
from apps.goods.models import Product


@require_http_methods(["POST"])
def cart_add(request: WSGIRequest) -> HttpResponseRedirect | HttpResponse:
    product_id = request.POST.get('product_id')
    product = Product.objects.get(pk=product_id)
    carts = Cart.objects.filter(
        session_key=request.session.session_key,
        product=product,
    )
    if carts.exists():
        cart = carts.first()
        if cart:
            cart.quantity += 1
            cart.save()
    else:
        Cart.objects.create(
            session_key=request.session.session_key,
            product=product,
            quantity=1,
        )
    user_cart = get_user_carts(request)
    cart_items_html = render_to_string(
        template_name='carts/includes/included_cart.html',
        context={
            'carts': user_cart,
        },
        request=request
    )

    response_data = {
        'message': 'Товар добавлен в корзину',
        'cart_items_html': cart_items_html,
    }

    return JsonResponse(response_data)


@require_http_methods(["POST"])
def cart_change(request: WSGIRequest) -> HttpResponseRedirect | HttpResponse:
    card_id = request.POST.get('cart_id', None)
    quantity = request.POST.get('quantity', None)

    cart = Cart.objects.get(id=card_id)
    cart.quantity = quantity
    cart.save()

    cart = get_user_carts(request=request)
    cart_items_html = render_to_string(
        template_name='carts/includes/included_cart.html',
        context={'carts': cart},
        request=request,
    )

    response_data = {
        'message': 'Колличество изменено',
        'cart_items_html': cart_items_html,
    }

    return JsonResponse(response_data)


@require_http_methods(["POST"])
def cart_remove(request: WSGIRequest) -> HttpResponseRedirect | HttpResponse:
    cart_id = request.POST.get('cart_id', None)
    cart = Cart.objects.get(pk=cart_id)
    quantity = cart.quantity
    cart.delete()

    user_cart = get_user_carts(request=request)
    cart_items_html = render_to_string(
        template_name='carts/includes/included_cart.html',
        context={
            'carts': user_cart,
        },
        request=request
    )

    response_data = {
        'message': 'Товар удален из корзины',
        'cart_items_html': cart_items_html,
        'quantity_deleted': quantity,
    }

    return JsonResponse(response_data)
