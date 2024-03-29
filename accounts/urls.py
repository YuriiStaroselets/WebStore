from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .import views


urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('buy/', csrf_exempt(views.CheckoutView.as_view()), name='payment'),
    path('buy/status/', csrf_exempt(views.Status.as_view()), name='status'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name="dashboard"),

    path('my_orders/', views.my_orders, name="my_orders"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('change_password/', views.change_password, name="change_password"),
    path('order_detail/<int:order_id>/', views.order_detail, name="order_detail"),

]


