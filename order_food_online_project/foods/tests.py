from django.test import TestCase, Client
from .models import Dish, Ingredient, Order, DishIngredients, OrderIngredients
from django.urls import reverse
from authentication.models import CustomUser


class OrderCreateTestCase(TestCase):

    def setUp(self):
        self.dish = Dish.objects.create(name="Borsh", description="Ukrainian national soup.")
        self.dish_invalid = Dish.objects.create(name="Invalid dish", description="Invalid dish description.")
        self.ingredient1 = Ingredient.objects.create(name="Beet", unit="gr")
        self.ingredient2 = Ingredient.objects.create(name="Tomato", unit="ml")
        self.dish_ingredient1 = DishIngredients.objects.create(dish=self.dish, ingredient=self.ingredient1,
                                                               quantity=200)
        self.dish_ingredient2 = DishIngredients.objects.create(dish=self.dish, ingredient=self.ingredient2,
                                                               quantity=100)
        self.user = CustomUser.objects.create_user(username="admin")
        self.user.set_password('123')

    def test_orders_template(self):
        url = reverse('order_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'foods/order_list.html')

    def test_order_add_valid(self):
        orders_count = Order.objects.count()
        self.client.post(reverse('order_add'),
                         {'ingredients': [self.ingredient1.id, self.ingredient2.id], 'status': 100, 'cost': 12.0,
                          'customer': self.user.id})
        self.assertEquals(Order.objects.count(), orders_count + 1)

    def test_order_add_invalid(self):
        orders_count = Order.objects.count()
        self.client.post(reverse('order_add'), {'dish_id': self.dish_invalid.id})
        self.assertNotEquals(Order.objects.count(), orders_count + 1)


class AddIngredientToDishTestCase(TestCase):

    def setUp(self):
        self.dish = Dish.objects.create(name="Borsh", description="Ukrainian national soup.")
        self.ingredient = Ingredient.objects.create(name="Beet", unit="gr")

    def test_add_ingredient_valid(self):
        data = {'csrfmiddlewaretoken': 'gzbeBISsoGAwMCr38PlKpe92QWqQZGNFE9yACElf578ZHWpPOr3M0g9ttoIvRNlu',
                'name': 'Borsh',
                'description': 'Ukrainian national soup.',
                'dishingredients_set-INITIAL_FORMS': '0',
                'dishingredients_set-TOTAL_FORMS': '1',
                'dishingredients_set-MAX_NUM_FORMS': '7',
                'dishingredients_set-MIN_NUM_FORMS': '0',
                'dishingredients_set-0-ingredient': self.ingredient.id,
                'dishingredients_set-0-quantity': '1',
                'dishingredients_set-0-dish': self.dish.id,
                'dishingredients_set-0-id': ''}
        count_before_add = DishIngredients.objects.count()
        dish_update_url = reverse('dish_edit', kwargs={'dish_id': self.dish.id})
        response = self.client.post(dish_update_url, data)
        count_after_add = DishIngredients.objects.count()
        self.assertEqual(count_before_add + 1, count_after_add)
        self.assertEqual(response.status_code, 302)

    def test_add_ingredient_invalid(self):
        data = {'csrfmiddlewaretoken': 'gzbeBISsoGAwMCr38PlKpe92QWqQZGNFE9yACElf578ZHWpPOr3M0g9ttoIvRNlu',
                'name': 'Borsh',
                'description': 'Ukrainian national soup.',
                'dishingredients_set-INITIAL_FORMS': '0',
                'dishingredients_set-TOTAL_FORMS': '1',
                'dishingredients_set-MAX_NUM_FORMS': '7',
                'dishingredients_set-MIN_NUM_FORMS': '0',
                'dishingredients_set-0-ingredient': self.ingredient.id,
                'dishingredients_set-0-quantity': '',
                'dishingredients_set-0-dish': self.dish.id,
                'dishingredients_set-0-id': ''}
        count_before_add = DishIngredients.objects.count()
        dish_update_url = reverse('dish_edit', kwargs={'dish_id': self.dish.id})
        response = self.client.post(dish_update_url, data)
        count_after_add = DishIngredients.objects.count()
        self.assertNotEqual(count_before_add + 1, count_after_add)
        self.assertEqual(response.status_code, 200)
