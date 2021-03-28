from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name = 'product-home'),
    path('add/',views.create_product, name = 'product-add'),
    path('edit/',views.edit_product, name = 'product-edit'),
    path('<int:p_id>/', views.edit_util, name='product_edit_util'),
    path('view/',views.view_product, name = 'product-view'),   
]

