from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Q
from .models import Dish, DishIngredients, Ingredient, OrderIngredients, Order, Section


def index(request):
    dishes = Dish.objects.all()
    return render(request, 'foods/index.html', context={'dishes': dishes})


def search(request):
    query = request.GET['query']
    if query:
        dishes = Dish.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        return render(request, 'foods/index.html', context={'dishes': dishes})
