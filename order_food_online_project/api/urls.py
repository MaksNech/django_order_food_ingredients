from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views as authtoken_views
from authentication.api_views import UserListView
from foods.api_views import SectionViewSet, IngredientViewSet, DishViewSet, OrderViewSet, DishIngredientsViewSet, \
    OrderIngredientsViewSet, CommentViewSet
from notes.api_views import NoteViewSet, NotedModelViewSet

router = routers.DefaultRouter()
router.register('sections', SectionViewSet)
router.register('comments', CommentViewSet)
router.register('ingredients', IngredientViewSet)
router.register('dishes', DishViewSet)
router.register('orders', OrderViewSet)
router.register('dish_ingredients', DishIngredientsViewSet)
router.register('order_ingredients', OrderIngredientsViewSet)
router.register('notes', NoteViewSet)
router.register('noted_models', NotedModelViewSet)

urlpatterns = [
    path('api-token-auth/', authtoken_views.obtain_auth_token),
    path('rest-auth/', include('rest_auth.urls')),
    path('users/', UserListView.as_view()),
    path('routes/', include((router.urls, 'app_name'), namespace='instance_name')),

]
