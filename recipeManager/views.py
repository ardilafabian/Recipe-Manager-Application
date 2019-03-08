from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Recipe, Ingredient, Recipe_Ingredients

class IndexView(generic.ListView):
    template_name = 'recipeManager/index.html'
    context_object_name = 'recipes_list'
    paginate_by = 8

    def get_queryset(self):
        return Recipe.objects.all()


def doSearch(searchTerm, ingredients):
    if searchTerm.isdigit():
        return ingredients.filter(id__icontains=searchTerm)
    else:
        return ingredients.filter(name__icontains=searchTerm)


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


class AddRecipeView(generic.ListView):
    context_object_name = 'ingredients_list'
    template_name = 'recipeManager/addRecipe.html'

    def get_queryset(self):
        ingredients = Ingredient.objects.all()
        if 'search' in self.request.GET:
            return doSearch(self.request.GET['search'], ingredients)
        else:
            return ingredients

def createRecipe(request):
    #print(request.POST)
    recipe = Recipe.objects.create(name=request.POST['name'],
                                   description=request.POST['description'])
    ingredients_id = request.POST.getlist('ingredient_id')
    quantities = request.POST.getlist('quantity')
    for i in range(len(ingredients_id)):
        ingredient = Ingredient.objects.get(pk=ingredients_id[i])
        relation = Recipe_Ingredients.objects.create(recipe=recipe,
                                                     ingredient=ingredient,
                                                     quantity=quantities[i])
    return HttpResponseRedirect(reverse('recipeManager:recipeDetail', args=(recipe.id,)))


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

def EditRecipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    context = {'recipe' : recipe}

    recipe_ingredients = Ingredient.objects.filter(recipe__id=recipe.id)
    if len(recipe_ingredients) > 0 : context['recipe_ingredients'] = recipe_ingredients
    ingredients_list = Ingredient.objects.all()
    if len(ingredients_list) > 0 : context['ingredients_list'] = ingredients_list

    return render(request, "recipeManager/editRecipe.html", context)


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
