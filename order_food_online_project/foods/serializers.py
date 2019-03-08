from rest_framework import serializers
from .models import Section, Ingredient, Dish, Order, DishIngredients, OrderIngredients, Comment
from authentication.serializers import UserSerializer


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('id', 'name', 'created_on')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'img', 'quantity', 'unit', 'cost', 'author', 'created_on')

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        author = UserSerializer.create(UserSerializer(), validated_data=author_data)
        ingredient, created = Ingredient.objects.update_or_create(

            name=validated_data.pop('name'),
            img=validated_data.pop('img'),
            quantity=validated_data.pop('quantity'),
            unit=validated_data.pop('unit'),
            cost=validated_data.pop('cost'),
            author=author,

        )
        return ingredient


class DishSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.username')
    slug = serializers.ReadOnlyField()
    section = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all(), allow_null=False, required=True)

    class Meta:
        model = Dish
        fields = ('id', 'name', 'slug', 'img', 'description', 'section', 'ingredients', 'author', 'created_on')


class OrderSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)
    customer = serializers.ReadOnlyField(source='customer.username')

    class Meta:
        model = Order
        fields = ('id', 'number', 'ingredients', 'cost', 'status', 'customer', 'created_on', 'updated_on')


class DishIngredientsSerializer(serializers.ModelSerializer):
    dish = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all(), allow_null=False, required=True)
    ingredient = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all(), allow_null=False, required=True)

    class Meta:
        model = DishIngredients
        fields = ('id', 'dish', 'ingredient', 'quantity')


class OrderIngredientsSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), allow_null=False, required=True)
    ingredient = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all(), allow_null=False, required=True)

    class Meta:
        model = OrderIngredients
        fields = ('id', 'order', 'ingredient', 'quantity', 'cost')


class CommentSerializer(serializers.ModelSerializer):
    dish = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all(), allow_null=False, required=True)
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ('id', 'dish', 'body', 'author')
