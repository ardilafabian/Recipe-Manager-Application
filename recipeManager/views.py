from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Recipe, Ingredient, Recipe_Ingredients

#----------------------------------------------------------------------------------------------------

class IndexView(generic.ListView):
    template_name = 'recipeManager/index.html'
    context_object_name = 'recipes_list'
    paginate_by = 8

    def get_queryset(self):
        return Recipe.objects.all()

#----------------------------------------------------------------------------------------------------

def doSearch(searchTerm, ingredients):
    if searchTerm.isdigit():
        return ingredients.filter(id__icontains=searchTerm)
    else:
        return ingredients.filter(name__icontains=searchTerm)

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

def AddRecipeView(request):
    ingredients_list = Ingredient.objects.all()

    if request.method == "POST":
        recipe = Recipe.objects.create(name=request.POST['name'],
                                       description=request.POST['description'])
        ingredients_id = request.POST.getlist('ingredient_id')
        quantities = request.POST.getlist('quantity')
        for i in range(len(ingredients_id)):
            ingredient = Ingredient.objects.get(pk=ingredients_id[i])
            Recipe_Ingredients.objects.create(recipe=recipe,
                                             ingredient=ingredient,
                                             quantity=quantities[i])
        return HttpResponseRedirect(reverse('recipeManager:recipeDetail', args=(recipe.id,)))

    context = {
        'ingredients_list' : ingredients_list,
        }
    return render(request, "recipeManager/addRecipe.html", context)

#----------------------------------------------------------------------------------------------------

class IngredientDetailView(generic.DetailView):
    model = Ingredient
    template_name = 'recipeManager/ingredientDetail.html'

#----------------------------------------------------------------------------------------------------

class AddIngredientView(generic.CreateView):
    model = Ingredient
    template_name = 'recipeManager/addIngredient.html'
    fields = ['name', 'cost', 'amount', 'unit']

    def get_success_url(self):
        return reverse('recipeManager:ingredientDetail', args=(self.object.id,))

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
    b = newIngredients
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
    self.assert_(len(oldQuantities) == len(newQuantities), 'Internal error at: validateQuantitiesChange')
    a, b = oldQuantities, newQuantities
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

def EditRecipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipe_ingredients = Ingredient.objects.filter(recipe__id=recipe.id)

    if request.method == "POST":
        print(request.POST)
        itChanged = False
        if recipe.name != request.POST['name']: recipe.name, itChanged = request.POST['name'], True
        if recipe.description != request.POST['description']: recipe.description, itChanged = request.POST['description'], True
        recipe_ingredients_id = request.POST.getlist('ingredient_id')
        newQuantities = request.POST.getlist('quantity')
        if not(validateIngredientsChange(recipe_ingredients, recipe_ingredients_id)) or not(validateQuantitiesChange(recipe, recipe_ingredients_id, newQuantities)):
            makeIngredientsChange(recipe, recipe_ingredients_id, newQuantities)
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
        ingredient.save()

    return HttpResponseRedirect(reverse('recipeManager:ingredientDetail', args=(ingredient.id,)))
