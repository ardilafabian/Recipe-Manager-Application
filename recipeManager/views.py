from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse

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
    #print(request.POST)
    ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
    itChanged = False

    if ingredient.name != request.POST['name']: ingredient.name, itChanged = request.POST['name'], True
    if ingredient.cost != request.POST['cost']: ingredient.cost, itChanged = request.POST['cost'], True
    if ingredient.amount != request.POST['amount']: ingredient.amount, itChanged = request.POST['amount'], True
    if ingredient.unit != request.POST['unit']: ingredient.unit, itChanged = request.POST['unit'], True

    if itChanged:
        ingredient.save()

    return HttpResponseRedirect(reverse('recipeManager:ingredientDetail', args=(ingredient.id,)))
