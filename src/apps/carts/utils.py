from django.core.handlers.wsgi import WSGIRequest

from apps.carts.models import Cart


def get_user_carts(request: WSGIRequest):
    if not request.session.session_key:
        request.session.create()

    return Cart.objects.filter(session_key=request.session.session_key).select_related('product')
