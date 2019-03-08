from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('permission/denied/', views.permission_denied, name='permission_denied'),
    path('ingredient/', views.ingredient_list, name='ingredient_list'),
    path('ingredient/search/', views.ingredient_search, name='ingredient_search'),
    path('ingredient/add/', views.ingredient_add, name='ingredient_add'),
    path('ingredient/view/<int:ingredient_id>/', views.ingredient_view, name='ingredient_view'),
    path('ingredient/edit/<int:ingredient_id>/', views.ingredient_edit, name='ingredient_edit'),
    path('ingredient/delete/<int:ingredient_id>/', views.ingredient_delete, name='ingredient_delete'),
    path('dish/', views.dish_list, name='dish_list'),
    path('dish/search/', views.dish_search, name='dish_search'),
    path('dish/add/', views.dish_add, name='dish_add'),
    path('dish/view/<slug:dish_slug>/', views.dish_view, name='dish_view'),
    path('dish/edit/<int:dish_id>/', views.dish_edit, name='dish_edit'),
    path('dish/delete/<int:dish_id>/', views.dish_delete, name='dish_delete'),
    path('cart/order/', views.order_list, name='order_list'),
    path('cart/order/search/', views.order_search, name='order_search'),
    path('cart/order/add/', views.order_add, name='order_add'),
    path('cart/order/view/<int:order_id>/', views.order_view, name='order_view'),

]
