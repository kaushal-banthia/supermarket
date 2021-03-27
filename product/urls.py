from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name = 'product-home'),
    path('add/',views.create_product, name = 'product-add'),
    path('edit/',views.edit_product, name = 'product-edit'),
    path('view/',views.view_product, name = 'product-view'),   
]

