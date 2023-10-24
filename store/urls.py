from django.urls import path
from .import views


urlpatterns = [
    path('', views.store, name='store'),
    path('main_category/<slug:main_category_slug>/<slug:category_slug>/<slug:sub_category_slug>/<slug:product_slug>', views.product_detail, name='product_detail'),
    
    path('search/', views.search, name="search"),
    path('filter', views.filter, name="filter"),

    path('submit_review/<int:product_id>/', views.submit_review, name="submit_review"),
]
