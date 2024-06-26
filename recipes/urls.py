from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

app_name = "recipes"

router = DefaultRouter()
router.register(r'recipes', views.RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:recipe_id>', views.recipe_detail, name='recipe_detail'),
    path('<int:recipe_id>/toogle_favorite', views.toogle_favorite, name='toogle_favorite'),
    path('my-favorites/', views.favorite_recipes, name='favorite_recipes'),
    path('search/', views.search_results, name='search_results'),
    path('<int:recipe_id>/delete/', views.delete_recipes, name='delete_recipes'),
    path('<int:recipe_id>/edit/', views.edit_recipe, name='edit_recipe'),
    path('api/', include(router.urls)),
]