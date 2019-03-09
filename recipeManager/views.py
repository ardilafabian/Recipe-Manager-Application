from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from .models import Recipe, Ingredient, Recipe_Ingredients

#----------------------------------------------------------------------------------------------------

def doSearch(searchTerm, list):
    if searchTerm.isdigit():
        return list.filter(id__icontains=searchTerm)
    else:
        return list.filter(name__icontains=searchTerm)

#----------------------------------------------------------------------------------------------------

class IndexView(generic.ListView):
    template_name = 'recipeManager/index.html'
    context_object_name = 'recipes_list'
    paginate_by = 8

    def get_queryset(self):
        recipes = Recipe.objects.all()
        if 'search' in self.request.GET:
            return doSearch(self.request.GET['search'], recipes)
        else:
            return recipes

#----------------------------------------------------------------------------------------------------

class IngredientsView(generic.ListView):
    template_name = 'recipeManager/ingredients.html'
    context_object_name = 'ingredients_list'
    paginate_by = 6

    def get_queryset(self):
        ingredients = Ingredient.objects.all()
        if 'search' in self.request.GET:
            return doSearch(self.request.GET['search'], ingredients)
        else:
            return ingredients

#----------------------------------------------------------------------------------------------------

#This function has the objective to be extensible and be able to add here any business validation needed
def CreationAndValidationRecipeModel(request):
    confirmation = True
    recipe = Recipe.objects.create(name=request['name'],
                                   description=request['description'])
    ingredients_id = request.getlist('ingredient_id')
    quantities = request.getlist('quantity')
    for i in range(len(ingredients_id)):
        ingredient = Ingredient.objects.get(pk=ingredients_id[i])
        Recipe_Ingredients.objects.create(recipe=recipe,
                                         ingredient=ingredient,
                                         quantity=quantities[i])
    return confirmation, recipe

#----------------------------------------------------------------------------------------------------

def AddRecipeView(request):
    ingredients_list = Ingredient.objects.all()

    if request.method == "POST":
        confirmation, recipe = CreationAndValidationRecipeModel(request.POST)
        if confirmation:
            messages.success(request, 'Recipe created successfully.', extra_tags='alert alert-success alert-dismissible fade show')
            return HttpResponseRedirect(reverse('recipeManager:recipeDetail', args=(recipe.id,)))
        else:
            messages.error(request, 'Something went wrong, try again later please.', extra_tags='alert alert-danger alert-dismissible fade show')
            return HttpResponseRedirect(reverse('recipeManager:addRecipe'))
    context = {
        'ingredients_list' : ingredients_list,
        }
    return render(request, "recipeManager/addRecipe.html", context)

#----------------------------------------------------------------------------------------------------

class IngredientDetailView(generic.DetailView):
    model = Ingredient
    template_name = 'recipeManager/ingredientDetail.html'

#----------------------------------------------------------------------------------------------------

#This function has the objective to be extensible and be able to add here any business validation needed
def CreationAndValidationIngredientModel(request):
    confirmation = True
    ingredient = Ingredient.objects.create(name=request['name'],
                                           cost=request['cost'],
                                           amount=request['amount'],
                                           unit=request['unit'])
    return confirmation, ingredient

#----------------------------------------------------------------------------------------------------

def AddIngredientView(request):
    choices_list = Ingredient.UNIT_CHOICES
    if request.method == "POST":
        confirmation, ingredient = CreationAndValidationIngredientModel(request.POST)
        if confirmation:
            messages.success(request, 'Ingredient created successfully.', extra_tags='alert alert-success alert-dismissible fade show')
            return HttpResponseRedirect(reverse('recipeManager:ingredientDetail', args=(ingredient.id,)))
        else:
            messages.error(request, 'Something went wrong, try again later please.', extra_tags='alert alert-danger alert-dismissible fade show')
            return HttpResponseRedirect(reverse('recipeManager:ingredients'))
    context = {'choices_list' : choices_list}
    return render(request, "recipeManager/addIngredient.html", context)

#----------------------------------------------------------------------------------------------------

def calculateCosts(recipe):
    ingredients = Ingredient.objects.filter(recipe__id=recipe.id)
    totalCost = 0
    ingredientsCosts = []
    for ingredient in ingredients:
        quant = Recipe_Ingredients.objects.get(recipe__id = recipe.id, ingredient__id = ingredient.id).quantity
        costPerQuantity = round((ingredient.cost / ingredient.amount) * quant, 2)
        totalCost += costPerQuantity
        ingredientsCosts.append((ingredient, quant, costPerQuantity))
    return ingredientsCosts, round(totalCost, 2)

#----------------------------------------------------------------------------------------------------

def RecipeDetailView(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredientsCosts, totalCost = calculateCosts(recipe)
    context = {
        'recipe' : recipe,
        'ingredientsCosts' : ingredientsCosts,
        'totalCost' : totalCost}
    return render(request, "recipeManager/recipeDetail.html", context)

#----------------------------------------------------------------------------------------------------

def validateIngredientsChange(oldIngredients, newIngredients):
    a = []
    for ingr in oldIngredients:
        a.append(ingr.id)
    b = newIngredients.copy()
    a.sort()
    b.sort()
    return a == b

#----------------------------------------------------------------------------------------------------

def validateQuantitiesChange(recipe, recipe_ingredients_id, newQuantities):
    oldQuantities = []
    for id in recipe_ingredients_id:
        ingredient = Ingredient.objects.get(pk=id)
        oldQuantities.append(Recipe_Ingredients.objects.get(recipe__id=recipe.id,
                                                ingredient__id=ingredient.id).quant)
    assert(len(oldQuantities) == len(newQuantities), 'Internal error at: validateQuantitiesChange')
    a, b = oldQuantities, newQuantities.copy()
    a.sort()
    b.sort()
    return a == b

#----------------------------------------------------------------------------------------------------

def makeIngredientsChange(recipe, recipe_ingredients_id, newQuantities):
    recipe.ingredients.clear()
    for i in range(len(recipe_ingredients_id)):
        Recipe_Ingredients.objects.create(recipe=recipe,
                                          ingredient=Ingredient.objects.get(pk=recipe_ingredients_id[i]),
                                          quantity=newQuantities[i])
#----------------------------------------------------------------------------------------------------

#This function has the objective to be extensible and be able to add here any business validation needed
def EditRecipeValidation(request, recipe, recipe_ingredients):
    confirmation = True
    if recipe.name != request['name']: Recipe.objects.filter(pk=recipe.id).update(name = request['name'])
    if recipe.description != request['description']: Recipe.objects.filter(pk=recipe.id).update(description = request['description'])
    recipe_ingredients_id = request.getlist('ingredient_id')
    newQuantities = request.getlist('quantity')
    if not(validateIngredientsChange(recipe_ingredients, recipe_ingredients_id)) or not(validateQuantitiesChange(recipe, recipe_ingredients_id, newQuantities)):
        makeIngredientsChange(recipe, recipe_ingredients_id, newQuantities)
    return confirmation


#----------------------------------------------------------------------------------------------------

def EditRecipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipe_ingredients = Ingredient.objects.filter(recipe__id=recipe.id)

    if request.method == "POST":
        confirmation = EditRecipeValidation(request.POST, recipe, recipe_ingredients)
        recipe = Recipe.objects.get(pk=recipe.id)
        if confirmation:
            messages.success(request, 'Recipe edited successfully.', extra_tags='alert alert-success alert-dismissible fade show')
        else:
            messages.error(request, 'Something went wrong, try again later please.', extra_tags='alert alert-danger alert-dismissible fade show')
        return HttpResponseRedirect(reverse('recipeManager:recipeDetail', args=(recipe.id,)))
    context = {'recipe' : recipe}

    ingredients_list = Ingredient.objects.all()
    if len(recipe_ingredients) > 0 : context['recipe_ingredients'] = recipe_ingredients
    if len(ingredients_list) > 0 : context['ingredients_list'] = ingredients_list

    ingredientsCosts, totalCost = calculateCosts(recipe)
    context['ingredientsCosts'] = ingredientsCosts

    return render(request, "recipeManager/editRecipe.html", context)

#----------------------------------------------------------------------------------------------------

def updateIngredient(request, ingredient_id):
    ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
    itChanged = False

    if ingredient.name != request.POST['name']: ingredient.name, itChanged = request.POST['name'], True
    if ingredient.cost != request.POST['cost']: ingredient.cost, itChanged = request.POST['cost'], True
    if ingredient.amount != request.POST['amount']: ingredient.amount, itChanged = request.POST['amount'], True
    if ingredient.unit != request.POST['unit']: ingredient.unit, itChanged = request.POST['unit'], True

    if itChanged:
        messages.success(request, 'Ingredient updated successfully.', extra_tags='alert alert-success alert-dismissible fade show')
        ingredient.save()

    return HttpResponseRedirect(reverse('recipeManager:ingredientDetail', args=(ingredient.id,)))
