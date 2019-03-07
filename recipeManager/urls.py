from django.urls import path
from . import views
from django.urls import reverse

app_name = 'recipeManager'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('add/', views.AddRecipeView.as_view(), name='addRecipe'),
    path('create/', views.createRecipe, name='createRecipe'),
    path('ingredients/', views.IngredientsView.as_view(), name='ingredients'),
    path('<int:recipe_id>/', views.RecipeDetailView, name='recipeDetail'),
    path('ingredient/<int:pk>/', views.IngredientDetailView.as_view(), name='ingredientDetail'),
    path('ingredient/<int:ingredient_id>/update/', views.updateIngredient, name='updateIngredient'),
    path('ingredients/add/', views.AddIngredientView.as_view(), name='addIngredient'),
]
