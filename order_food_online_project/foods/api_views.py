from rest_framework import viewsets
from .models import Section, Ingredient, Dish, Order, DishIngredients, OrderIngredients
from .serializers import SectionSerializer, IngredientSerializer, DishSerializer, OrderSerializer, \
    DishIngredientsSerializer, OrderIngredientsSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsAuthorOrReadOnly, IsCustomerOrReadOnly


class SectionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Section.objects.all()
    serializer_class = SectionSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class DishViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = (IsCustomerOrReadOnly,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class DishIngredientsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = DishIngredients.objects.all()
    serializer_class = DishIngredientsSerializer


class OrderIngredientsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = OrderIngredients.objects.all()
    serializer_class = OrderIngredientsSerializer
