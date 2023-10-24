from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .import views


urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('payments/<int:order_number>/', csrf_exempt(views.payments), name='payments'),
    path('payments/status/', csrf_exempt(views.payments_status), name='payment_status'),
    path('order_complete/', views.order_complete, name='order_complete'),
]
