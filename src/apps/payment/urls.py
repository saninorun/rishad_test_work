from django.urls import path
from apps.payment.views import SuccessView, CancelView, CreateCheckoutSessionView

app_name = 'payment'

urlpatterns = [
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session')
]
