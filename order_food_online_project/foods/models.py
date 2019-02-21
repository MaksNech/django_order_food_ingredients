import uuid
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Section(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Name: {}".format(self.name)

    class Meta:
        ordering = ['name']


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    img = models.ImageField(upload_to='ingredients/', null=True)
    quantity = models.DecimalField(max_digits=6, default=10, decimal_places=1, null=True)
    unit = models.CharField(max_length=20)
    cost = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Name: {} | Unit: {} | Quantity: {} | Cost: {}".format(self.name, self.unit, self.quantity, self.cost)

    class Meta:
        ordering = ['-created_on']


# delete img with ingredient instance
@receiver(post_delete, sender=Ingredient)
def ingredient_img_delete(sender, instance, **kwargs):
    instance.img.delete(False)


class Dish(models.Model):
    name = models.CharField(max_length=100, unique=True)
    img = models.ImageField(upload_to='dishes/', null=True)
    description = models.CharField(max_length=300, null=True)
    section = models.ForeignKey('Section', on_delete=models.CASCADE, related_name='dishes', null=True)
    ingredients = models.ManyToManyField('Ingredient', through='DishIngredients', through_fields=('dish', 'ingredient'),
                                         related_name='dishes')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Name: {} | Section: {}".format(self.name, self.section)

    class Meta:
        ordering = ['-created_on']


# delete img with dish instance
@receiver(post_delete, sender=Dish)
def dish_img_delete(sender, instance, **kwargs):
    instance.img.delete(False)


class DishIngredients(models.Model):
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE, related_name='dish_ingredients', null=True)
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE, related_name='dish_ingredients', null=True)
    quantity = models.DecimalField(max_digits=6, decimal_places=1, null=True)

    def __str__(self):
        return "Dish: {} | Ingredient: {} | Quantity: {}".format(self.dish, self.ingredient, self.quantity)

    class Meta:
        ordering = ['dish__name']


class Order(models.Model):
    UNFULFILLED = 100
    FULFILLED = 200
    CANCELED = 300
    STATUS = (
        (UNFULFILLED, 'unfulfilled'),
        (FULFILLED, 'fulfilled'),
        (CANCELED, 'canceled'),
    )
    number = models.UUIDField(default=uuid.uuid1, editable=False)
    customer = models.CharField(max_length=200, blank=True)
    ingredients = models.ManyToManyField('Ingredient', through='OrderIngredients',
                                         through_fields=('order', 'ingredient'), related_name='orders')
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    status = models.IntegerField(
        choices=STATUS,
        default=UNFULFILLED,
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Number: {} | Created: {} | Status: {} | Updated: {} | Cost: {}".format(self.number, self.created_on,
                                                                                       self.status,
                                                                                       self.updated_on, self.cost)

    class Meta:
        ordering = ['created_on']


class OrderIngredients(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_ingredients', null=True)
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE, related_name='order_ingredients', null=True)
    quantity = models.DecimalField(max_digits=6, decimal_places=1)
    cost = models.DecimalField(max_digits=9, decimal_places=2, null=True)

    def __str__(self):
        return "Order: {} | Ingredient: {} | Quantity: {} | Cost: {}".format(self.order, self.ingredient, self.quantity,
                                                                             self.cost)
