from django.urls import path
from . import views

urlpatterns = [
    path('souvenirs', views.souvenirs),
    path('food', views.food),
    path('natural_products', views.natural_products),
    path('Leather_accessories', views.Leather_accessories),
    path('cart', views.cart),
    path('order', views.order),
    path('checkout', views.checkout),
    path('process_cart/<id>', views.process_cart),
    path('remove_cart/<id>', views.remove_cart),
    path('checkout', views.checkout),
    path('place_order', views.place_order),
    path('search', views.search),
]

