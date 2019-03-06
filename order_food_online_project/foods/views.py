from decimal import Decimal
from django.shortcuts import render
from django.urls import reverse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from .models import Dish, DishIngredients, Ingredient, OrderIngredients, Order, Section
from .forms import DishAddForm, IngredientAddForm, OrderAddForm
from .models import get_allowed_groups


def permission_denied(request):
    permission_codename = request.session.get('permission_codename')
    data = get_allowed_groups(permission_codename)
    return render(request, 'foods/permission_denied.html',
                  context={'allowed_groups': data['allowed_groups'], 'permission': data['permission']})


def index(request):
    dishes = Dish.objects.all()[:9]

    return render(request, 'foods/index.html', context={'dishes': dishes})


def ingredient_list(request):
    ingredients = Ingredient.objects.all()
    return render(request, 'foods/ingredient_list.html', context={'ingredients': ingredients})


def ingredient_search(request):
    query = request.GET['query']
    if query:
        ingredients = Ingredient.objects.filter(Q(name__icontains=query))
        return render(request, 'foods/ingredient_list.html', context={'ingredients': ingredients})


def ingredient_add(request):
    if request.user.has_perm('foods.add_ingredient'):

        if request.method == "POST":
            form = IngredientAddForm(request.POST, request.FILES)
            if form.is_valid():
                ingredient = form.save(commit=False)
                ingredient.author = request.user
                ingredient.save()
                return HttpResponseRedirect(reverse('ingredient_list'))

        form = IngredientAddForm()

        return render(request, 'foods/ingredient_add.html', context={'form': form})
    else:
        request.session['permission_codename'] = 'add_ingredient'
        return HttpResponseRedirect(reverse('permission_denied'))


def ingredient_view(request, ingredient_id):
    ingredient = Ingredient.objects.get(id=ingredient_id)
    if ingredient:
        return render(request, 'foods/ingredient_view.html', context={'ingredient': ingredient})


def ingredient_edit(request, ingredient_id):
    if request.user.has_perm('foods.change_ingredient'):

        ingredient = Ingredient.objects.get(id=ingredient_id)
        if ingredient:

            if request.method == "POST":
                form = IngredientAddForm(request.POST, request.FILES, instance=ingredient)
                if form.is_valid():
                    form.save()

                    return HttpResponseRedirect(reverse('ingredient_list'))

            form = IngredientAddForm()

            return render(request, 'foods/ingredient_edit.html', context={'ingredient': ingredient, 'form': form})
    else:
        request.session['permission_codename'] = 'change_ingredient'
        return HttpResponseRedirect(reverse('permission_denied'))


def ingredient_delete(request, ingredient_id):
    if request.user.has_perm('foods.delete_ingredient'):

        ingredient = Ingredient.objects.get(id=ingredient_id)

        if ingredient:
            if request.method == "POST":
                ingredient.delete()
                return HttpResponseRedirect(reverse('ingredient_list'))
    else:
        request.session['permission_codename'] = 'delete_ingredient'
        return HttpResponseRedirect(reverse('permission_denied'))


def dish_list(request):
    dishes = Dish.objects.all()
    return render(request, 'foods/dish_list.html', context={'dishes': dishes})


def dish_search(request):
    query = request.GET['query']
    if query:
        dishes = Dish.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        return render(request, 'foods/dish_list.html', context={'dishes': dishes})


def dish_add(request):
    if request.user.has_perm('foods.add_dish'):

        if request.method == "POST":
            form = DishAddForm(request.POST, request.FILES)
            if form.is_valid():

                new_dish = form.save(commit=False)
                new_dish.author = request.user

                ingredients_obj = []
                ingredients_id = request.POST.getlist("dish_ingredient_added")
                quantity = request.POST.getlist("dish_ingredient_quantity_added")
                for ingredient_id in ingredients_id:
                    ingredient_obj = Ingredient.objects.get(id=int(ingredient_id))
                    ingredients_obj.append(ingredient_obj)

                data = dict(zip(ingredients_obj, quantity))
                new_dish.save()

                for key, val in data.items():
                    DishIngredients.objects.create(dish=new_dish, ingredient=key, quantity=val)

                return HttpResponseRedirect(reverse('dish_list'))

        form = DishAddForm()
        sections = Section.objects.all()
        ingredients = Ingredient.objects.all()
        dish_ingredients = DishIngredients.objects.all()
        return render(request, 'foods/dish_add.html',
                      context={'ingredients': ingredients, 'sections': sections, 'dish_ingredients': dish_ingredients,
                               'form': form})
    else:
        request.session['permission_codename'] = 'add_dish'
        return HttpResponseRedirect(reverse('permission_denied'))


def dish_view(request, dish_id):
    dish = Dish.objects.get(id=dish_id)
    dish_ingredients = DishIngredients.objects.filter(dish__id=dish_id)
    ingredients = []
    if dish_ingredients:
        for dish_ingredient in dish_ingredients:
            ingredient = Ingredient.objects.get(id=dish_ingredient.ingredient.id)
            ingredients.append({"id": ingredient.id, "name": ingredient.name, "quantity": dish_ingredient.quantity,
                                "unit": ingredient.unit})

    if dish:
        return render(request, 'foods/dish_view.html', context={'dish': dish, 'ingredients': ingredients})


def dish_edit(request, dish_id):
    if request.user.has_perm('foods.change_dish'):

        dish = Dish.objects.get(id=dish_id)

        if dish:

            if request.method == "POST":
                form = DishAddForm(request.POST, request.FILES, instance=dish)
                if form.is_valid():

                    edit_dish = form.save()

                    DishIngredients.objects.filter(dish__id=edit_dish.id).delete()

                    ingredients_obj = []
                    ingredients_id = request.POST.getlist("dish_ingredient_added")
                    quantity = request.POST.getlist("dish_ingredient_quantity_added")
                    for ingredient_id in ingredients_id:
                        ingredient_obj = Ingredient.objects.get(id=int(ingredient_id))
                        ingredients_obj.append(ingredient_obj)

                    data = dict(zip(ingredients_obj, quantity))

                    for key, val in data.items():
                        DishIngredients.objects.create(dish=edit_dish, ingredient=key, quantity=val)
                    return HttpResponseRedirect(reverse('dish_list'))

            form = DishAddForm()
            sections = Section.objects.all()
            ingredients = Ingredient.objects.all()
            dish_ingredients = DishIngredients.objects.filter(dish=dish_id)

            return render(request, 'foods/dish_edit.html',
                          context={'dish': dish, 'ingredients': ingredients, 'sections': sections,
                                   'dish_ingredients': dish_ingredients, 'form': form})
    else:
        request.session['permission_codename'] = 'change_dish'
        return HttpResponseRedirect(reverse('permission_denied'))


def dish_delete(request, dish_id):
    if request.user.has_perm('foods.delete_dish'):

        dish = Dish.objects.get(id=dish_id)

        if dish:
            if request.method == "POST":
                dish.delete()
                return HttpResponseRedirect(reverse('dish_list'))
    else:
        request.session['permission_codename'] = 'delete_dish'
        return HttpResponseRedirect(reverse('permission_denied'))


def order_list(request):
    if request.user.has_perm('foods.view_order'):

        orders = Order.objects.all()
        return render(request, 'foods/order_list.html', context={'orders': orders})
    else:
        request.session['permission_codename'] = 'view_order'
        return HttpResponseRedirect(reverse('permission_denied'))


def order_search(request):
    if request.user.has_perm('foods.view_order'):

        query = request.GET['query']
        if query:
            orders = Order.objects.filter(Q(number__icontains=query) | Q(customer__icontains=query))
            return render(request, 'foods/order_list.html', context={'orders': orders})
    else:
        request.session['permission_codename'] = 'view_order'
        return HttpResponseRedirect(reverse('permission_denied'))


def order_add(request):
    if request.user.has_perm('foods.add_order'):

        if request.method == "POST":
            form = OrderAddForm(request.POST, request.FILES)
            if form.is_valid():
                ordered_ingredients_list = request.POST.getlist("order_ingredient")
                total_cost = 0
                for ordered_ingredient in ordered_ingredients_list:
                    data = ordered_ingredient.split('|')
                    total_cost += Decimal(data[2])

                form.cleaned_data['cost'] = total_cost

                new_order = form.save(commit=False)
                new_order.customer = request.user
                new_order.save()

                for ordered_ingredient in ordered_ingredients_list:
                    data = ordered_ingredient.split('|')
                    ingredient_id = data[0]
                    ingredient_quantity = data[1]
                    ingredient_cost = data[2]
                    added_ingred = Ingredient.objects.get(id=int(ingredient_id))
                    OrderIngredients.objects.create(order=new_order, ingredient=added_ingred,
                                                    quantity=ingredient_quantity, cost=ingredient_cost)
                return HttpResponseRedirect(reverse('order_list'))

        form = OrderAddForm()

        ingredients = Ingredient.objects.all()

        return render(request, 'foods/order_add.html',
                      context={'ingredients': ingredients, 'form': form})
    else:
        request.session['permission_codename'] = 'add_order'
        return HttpResponseRedirect(reverse('permission_denied'))


def order_view(request, order_id):
    if request.user.has_perm('foods.view_order'):

        order = Order.objects.get(id=order_id)

        order_ingredients = OrderIngredients.objects.filter(order__id=order_id)
        ingredients = []
        if order_ingredients:
            for order_ingredient in order_ingredients:
                ingredient = Ingredient.objects.get(id=order_ingredient.ingredient.id)
                ingredients.append({"id": ingredient.id, "name": ingredient.name, "cost": order_ingredient.cost,
                                    "quantity": order_ingredient.quantity,
                                    "unit": ingredient.unit})

        if order:
            return render(request, 'foods/order_view.html', context={'order': order, 'ingredients': ingredients})
    else:
        request.session['permission_codename'] = 'view_order'
        return HttpResponseRedirect(reverse('permission_denied'))
