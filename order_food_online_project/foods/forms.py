from django.db import models
from django.forms import ModelForm
from django import forms
from .models import Dish, DishIngredients, Ingredient, OrderIngredients, Order, Section

class DishAddForm(ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'img', 'description', 'section']

