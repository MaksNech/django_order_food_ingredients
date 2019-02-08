from django.contrib import admin

from .models import Ingredient, Dish, Order, Section, DishIngredients, OrderIngredients


class DishIngredientsInline(admin.TabularInline):
    model = DishIngredients
    extra = 1


class OrderIngredientsInline(admin.TabularInline):
    model = OrderIngredients
    extra = 1


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit')
    list_filter = ('name', 'unit',)
    inlines = (DishIngredientsInline, OrderIngredientsInline,)
    search_fields = ('name',)


class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'section')
    list_filter = ('name', 'section',)
    inlines = (DishIngredientsInline,)
    search_fields = ('name',)


class DishIngredientsAdmin(admin.ModelAdmin):
    list_display = ('dish', 'ingredient', 'quantity')
    list_filter = ('dish', 'ingredient',)
    search_fields = ('dish__name', 'ingredient__name')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('number', 'customer', 'cost', 'status')
    list_filter = ('status', 'customer')
    inlines = (OrderIngredientsInline,)
    search_fields = ('number', 'customer')


class OrderIngredientsAdmin(admin.ModelAdmin):
    list_display = ('order', 'ingredient', 'quantity', 'cost',)
    list_filter = ('ingredient',)
    search_fields = ('order__number', 'ingredient__name')


admin.site.register(Section)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Dish, DishAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(DishIngredients, DishIngredientsAdmin)
admin.site.register(OrderIngredients, OrderIngredientsAdmin)
