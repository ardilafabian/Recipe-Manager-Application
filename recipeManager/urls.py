from django.urls import path
from . import views

app_name = 'recipeManager'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('ingredients/', views.IngredientsView.as_view(), name='ingredients'),
    path('<int:pk>/', views.RecipeDetailView.as_view(), name='recipeDetail'),
    path('ingredient/<int:pk>/', views.IngredientDetailView.as_view(), name='ingredientDetail')
]
