from django.urls import path
from django.views import View
from .import views

urlpatterns = [
    path('', views.adminpanel, name="adminpanel"),
    
    path('user_accounts_table/<int:id>', views.user_accounts_table, name="user_accounts_table"),
    path('cart_table/<int:id>', views.cart_table, name="cart_table"),
    path('category_table/<int:id>/', views.category_table, name="category_table"),
    path('order_table/<int:id>/', views.order_table, name='order_table'),
    path('store_table/<int:id>/', views.store_table, name="store_table"),
    path('home_table/<int:id>/', views.home_table, name="home_table"),

    path('ban_user/<int:id>/', views.ban_user, name="ban_user"),
    path('unban_user/<int:id>/', views.unban_user, name='unban_user'),
    
    path('add_main_category/', views.add_main_category, name="add_main_category"),
    path('edit_main_category/<int:id>/', views.edit_main_category, name="edit_main_category"),
    path('delete_main_category/<int:id>/', views.delete_main_category, name="delete_main_category"),

    path('add_category/', views.add_category, name="add_category"),
    path('edit_category/<int:id>/', views.edit_category, name="edit_category"),
    path('delete_category/<int:id>/', views.delete_category, name='delete_category'),

    path('add_sub_category/', views.add_sub_category, name="add_sub_category"),
    path('edit_sub_category/<int:id>/', views.edit_sub_category, name="edit_sub_category"),
    path('delete_sub_category/<int:id>/', views.delete_sub_category, name="delete_sub_category"),

    path('add_brand/', views.add_brand, name="add_brand"),
    path('edit_brand/<int:id>/', views.edit_brand, name="edit_brand"),
    path('delete_brand/<int:id>/', views.delete_brand, name="delete_brand"),

    path('add_product/', views.add_product, name="add_product"),
    path('edit_product/<int:id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:id>/', views.delete_product, name="delete_product"),

    path('add_variations/',views.add_variations,name="add_variations"),
    path('edit_variations/<int:id>/',views.edit_variations,name='edit_variations'),
    path('delete_variatons/<int:id>/',views.delete_variatons,name="delete_variatons"),

    path('add_carousels/',views.add_carousels,name="add_carousels"),
    path('edit_carousel/<int:id>/',views.edit_carousel,name='edit_carousel'),
    path('carousel_not_available/<int:id>/',views.carousel_not_available,name="carousel_not_available"),
    path('caraousel_available/<int:id>/',views.caraousel_available,name='caraousel_available'),
    path('delete_carousel/<int:id>/',views.delete_carousel,name="delete_carousel"),

    path('order_accepted/<int:order_id>',views.order_accepted,name="order_accepted"),
    path('order_completed/<int:order_id>',views.order_completed,name="order_completed"),
    path('order_cancelled/<int:order_id>',views.order_cancelled,name="order_cancelled"),
    path('order_items/<int:order_id>',views.order_items,name="order_items"),

    path('admin_search',views.admin_search,name="admin_search")




    
]
