from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Recipe, Ingredient, Recipe_Ingredients

class IndexView(generic.ListView):
    template_name = 'recipeManager/index.html'
    context_object_name = 'recipes_list'

    def get_queryset(self):
        return Recipe.objects.all()

class IngredientsView(generic.ListView):
    template_name = 'recipeManager/ingredients.html'
    context_object_name = 'ingredients_list'

    def get_queryset(self):
        # TDOD: refactor functions
        ingredients = Ingredient.objects.all()
        if 'search' in self.request.GET:
            searchTerm = self.request.GET['search']
            if searchTerm.isdigit():
                return ingredients.filter(id__icontains=searchTerm)
            else:
                return ingredients.filter(name__icontains=searchTerm)
        else:
            return ingredients

class IngredientDetailView(generic.DetailView):
    model = Ingredient
    template_name = 'recipeManager/ingredientDetail.html'

class AddIngredientView(generic.CreateView):
    model = Ingredient
    template_name = 'recipeManager/addIngredient.html'
    fields = ['name', 'cost', 'amount', 'unit']

    def get_success_url(self):
        return reverse('recipeManager:ingredientDetail', args=(self.object.id,))

def calculateCosts(recipe):
    ingredients = Ingredient.objects.filter(recipe__id=recipe.id)
    totalCost = 0
    ingredientsCosts = []
    for ingredient in ingredients:
        quant = Recipe_Ingredients.objects.get(recipe__id = recipe.id, ingredient__id = ingredient.id).quantity
        costPerQuantity = round((ingredient.cost / ingredient.amount) * quant, 2)
        totalCost += costPerQuantity
        ingredientsCosts.append((ingredient, quant, costPerQuantity))
    return ingredientsCosts, totalCost

def RecipeDetailView(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredientsCosts, totalCost = calculateCosts(recipe)
    context = {
        'recipe' : recipe,
        'ingredientsCosts' : ingredientsCosts,
        'totalCost' : totalCost}
    return render(request, "recipeManager/recipeDetail.html", context)

def updateIngredient(request, ingredient_id):
    ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
    itChanged = False

    # TODO: refactor functions, delegate
    if ingredient.name != request.POST['name']: ingredient.name, itChanged = request.POST['name'], True
    if ingredient.cost != request.POST['cost']: ingredient.cost, itChanged = request.POST['cost'], True
    if ingredient.amount != request.POST['amount']: ingredient.amount, itChanged = request.POST['amount'], True
    if ingredient.unit != request.POST['unit']: ingredient.unit, itChanged = request.POST['unit'], True

    if itChanged:
        ingredient.save()

    return HttpResponseRedirect(reverse('recipeManager:ingredientDetail', args=(ingredient.id,)))
