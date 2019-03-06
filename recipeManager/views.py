from django.shortcuts import render
from django.views import generic

from .models import Recipe, Ingredient

class IndexView(generic.ListView):
    template_name = 'recipeManager/index.html'
    context_object_name = 'recipes_list'

    def get_queryset(self):
        return Recipe.objects.all()

class IngredientsView(generic.ListView):
    template_name = 'recipeManager/ingredients.html'
    context_object_name = 'ingredients_list'

    def get_queryset(self):
        return Ingredient.objects.all()

class RecipeDetailView(generic.DetailView):
    model = Recipe
    template_name = 'recipeManager/recipeDetail.html'

class IngredientDetailView(generic.DetailView):
    model = Ingredient
    template_name = 'recipeManager/ingredientDetail.html'

def updateIngredient(request, ingredient_id):
    print(request.POST)
    return render(request, 'recipeManager/ingredientDetail.html', {'ingredient':Ingredient.objects.get(pk=1)})
