from django.contrib import admin

from .models import Ingredient, Dish, Order, Section, DishIngredients, OrderIngredients, Comment


class DishIngredientsInline(admin.TabularInline):
    model = DishIngredients
    extra = 1


class OrderIngredientsInline(admin.TabularInline):
    model = OrderIngredients
    extra = 1


class DishCommentInline(admin.TabularInline):
    model = Comment
    extra = 1


class SectionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('dish', 'author', 'body',)
    list_filter = ('dish', 'author',)
    search_fields = ('dish', 'author',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit')
    list_filter = ('name', 'unit',)
    inlines = (DishIngredientsInline, OrderIngredientsInline,)
    search_fields = ('name',)


class DishAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'section', 'slug')
    list_filter = ('name', 'section',)
    inlines = (DishIngredientsInline, DishCommentInline)
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


admin.site.register(Section, SectionAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Dish, DishAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(DishIngredients, DishIngredientsAdmin)
admin.site.register(OrderIngredients, OrderIngredientsAdmin)
