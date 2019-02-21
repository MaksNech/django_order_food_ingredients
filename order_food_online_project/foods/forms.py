from django.db import models
from django.forms import ModelForm, ValidationError

from .models import Dish, DishIngredients, Ingredient, OrderIngredients, Order, Section


class IngredientAddForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'img', 'quantity', 'unit', 'cost']


class DishAddForm(ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'img', 'description', 'section']


class OrderAddForm(ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'cost']
