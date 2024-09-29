from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
    path('payment/success/', views.payment_success, name='payment_success'),
]