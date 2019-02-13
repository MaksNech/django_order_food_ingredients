from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ingredient/', views.ingredient_list, name='ingredient_list'),
    path('ingredient/search/', views.ingredient_search, name='ingredient_search'),
    path('ingredient/add/', views.ingredient_add, name='ingredient_add'),
    path('ingredient/view/<int:ingredient_id>/', views.ingredient_view, name='ingredient_view'),
    path('ingredient/edit/', views.ingredient_edit, name='ingredient_edit'),
    path('ingredient/edit/update/', views.ingredient_edit_update, name='ingredient_edit_update'),
    path('ingredient/edit/delete/', views.ingredient_edit_delete, name='ingredient_edit_delete'),
    path('dish/', views.dish_list, name='dish_list'),
    path('dish/search/', views.dish_search, name='dish_search'),
    path('dish/add/', views.dish_add, name='dish_add'),
    path('dish/add/ingredient/', views.dish_add_ingredient, name='dish_add_ingredient'), #ajax request
    path('dish/view/<int:dish_id>/', views.dish_view, name='dish_view'),
    path('dish/edit/', views.dish_edit, name='dish_edit'),
    path('dish/edit/update/', views.dish_edit_update, name='dish_edit_update'),
    path('dish/edit/delete/', views.dish_edit_delete, name='dish_edit_delete'),

]
