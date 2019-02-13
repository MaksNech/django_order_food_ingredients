import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.db.models import Q
from .models import Dish, DishIngredients, Ingredient, OrderIngredients, Order, Section



def index(request):
    return render(request, 'foods/index.html', context={})


def ingredient_list(request):
    ingredients = Ingredient.objects.all()
    return render(request, 'foods/ingredient_list.html', context={'ingredients': ingredients})


def ingredient_search(request):
    query = request.GET['query']
    if query:
        ingredients = Ingredient.objects.filter(Q(name__icontains=query))
        return render(request, 'foods/ingredient_list.html', context={'ingredients': ingredients})


def ingredient_add(request):
    return render(request, 'foods/ingredient_add.html', context={})


def ingredient_view(request, ingredient_id):
    ingredient = Ingredient.objects.get(id=ingredient_id)
    if ingredient:
        return render(request, 'foods/ingredient_view.html', context={'ingredient': ingredient})


def ingredient_edit(request):
    pass


def ingredient_edit_update(request):
    pass


def ingredient_edit_delete(request):
    pass


def dish_list(request):
    dishes = Dish.objects.all()
    return render(request, 'foods/dish_list.html', context={'dishes': dishes})


def dish_search(request):
    query = request.GET['query']
    if query:
        dishes = Dish.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        return render(request, 'foods/dish_list.html', context={'dishes': dishes})


def dish_add(request):

    if request.method == "POST":

        dish_name=request.POST.get("dish_name")
        dish_desc=request.POST.get("dish_desc")
        dish_section = Section.objects.get(id=int(request.POST.get("dish_section")))
        new_dish = Dish(name=dish_name, description=dish_desc, section=dish_section)
        new_dish.save()

        ingredients_id_list=request.session['dish_ingredients_dict'].keys()
        ingredients_id_list = list(map(int, ingredients_id_list))
        # for ingredient_id in ingredients_id_list:
        #     added_ingred=Ingredient.objects.get(id=int(ingredient_id))
        #     new_dish.ingredients.add(added_ingred)
        #     new_dish.save()


        pass

        # ingredients.set(ingredients_id_list)
        # if new_dish.id:
        #
        #    return HttpResponseRedirect('')



    request.session['dish_ingredients_dict']={}
    sections = Section.objects.all()
    ingredients = Ingredient.objects.all()
    dish_ingredients = DishIngredients.objects.all()


    return render(request, 'foods/dish_add.html',
                      context={'ingredients': ingredients, 'sections': sections, 'dish_ingredients': dish_ingredients})


def dish_add_ingredient(request):
    if request.method == 'POST':

        if request.POST.get('action') == 'delete':

            id_deleted_ingredient = request.POST.get('id_deleted_ingredient')
            ingredient = Ingredient.objects.get(id=id_deleted_ingredient)
            dish_ingredients_dict=request.session['dish_ingredients_dict']
            dish_ingredients_dict.pop(str(ingredient.id), None)
            request.session['dish_ingredients_dict']=dish_ingredients_dict

            return JsonResponse({'msg': 'Ingredient removed!' })

        elif request.POST.get('action') == 'add':

            dish_ingredients_dict = {}
            new_added_ingredient = {}
            ingredient_id = request.POST.get('ingredient_id')
            ingredient_quantity = request.POST.get('ingredient_quantity')

            if ingredient_id and ingredient_quantity:

                ingredient = Ingredient.objects.get(id=ingredient_id)
                new_added_ingredient = {'id': ingredient.id, 'name': ingredient.name, 'quantity': ingredient_quantity,
                                        'unit': ingredient.unit}
                dish_ingredients_dict = request.session['dish_ingredients_dict']
                dish_ingredients_dict[ingredient.id] = ingredient_quantity
                request.session['dish_ingredients_dict'] = dish_ingredients_dict

            return JsonResponse(
                {'dish_ingredients_dict': dish_ingredients_dict, 'new_added_ingredient': new_added_ingredient, })


def dish_view(request, dish_id):
    dish = Dish.objects.get(id=dish_id)
    if dish:
        return render(request, 'foods/dish_view.html', context={'dish': dish})


def dish_edit(request):
    pass


def dish_edit_update(request):
    pass


def dish_edit_delete(request):
    pass
