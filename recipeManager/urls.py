from django.urls import path
from . import views
from django.urls import reverse

app_name = 'recipeManager'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('add/', views.AddRecipeView, name='addRecipe'),
    path('ingredients/', views.IngredientsView.as_view(), name='ingredients'),
    path('<int:recipe_id>/', views.RecipeDetailView, name='recipeDetail'),
    path('<int:recipe_id>/edit', views.EditRecipe, name='editRecipe'),
    path('ingredient/<int:pk>/', views.IngredientDetailView.as_view(), name='ingredientDetail'),
    path('ingredient/<int:ingredient_id>/update/', views.updateIngredient, name='updateIngredient'),
    path('ingredients/add/', views.AddIngredientView, name='addIngredient'),
]
