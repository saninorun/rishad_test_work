import stripe
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from apps.carts.models import Cart
from apps.carts.utils import get_user_carts

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(View):
    def post(self, request: WSGIRequest, *args, **kwargs):
        success_url = request.build_absolute_uri(reverse('payment:success'))
        success_url = request.build_absolute_uri()
        ddd = "http://localhost:8000/" + (reverse('payment:cancel')),
        user_cart = get_user_carts(request=request)
        order = []
        for cart in user_cart:
            order_item = {
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': 100 * round(cart.product.price, 0),
                    'product_data': {
                        'name': cart.product.title,
                    },
                },
                'quantity': cart.quantity,
            }
            order.append(order_item)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=order,
            metadata={
                "product_id": 1,
            },
            mode='payment',
            success_url=request.build_absolute_uri(reverse('payment:success')),
            cancel_url=request.build_absolute_uri(reverse('payment:cancel')),
        )
        return JsonResponse({
            'id': checkout_session.id
        })


class SuccessView(View):
    def get(self, request: WSGIRequest, *args, **kwargs):
        Cart.objects.filter(session_key=request.session.session_key).delete()
        request.session.delete()
        return render(request, "payment/success.html")


class CancelView(TemplateView):
    template_name = "payment/cancel.html"
