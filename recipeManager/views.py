from django.shortcuts import render
from django.views import generic

from .models import Recipe, Ingredient

class IndexView(generic.ListView):
    template_name = 'recipeManager/index.html'
    context_object_name = 'recipes_list'

    def get_queryset(self):
        return Recipe.objects.all()
