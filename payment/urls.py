from django.urls import path
from payment import views
from django.conf import settings


urlpatterns = [
    path('mpesa-payment/', views.mpesa_payment, name='mpesa_payment'),
    path('payment/', views.payment_view, name='payment'),]
