from django.db import models

class Ingredient(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    cost = models.FloatField()
    amount = models.FloatField()
    #-Unit Choices----
    GRAMS='g'
    KILOGRAMS='Kg'
    CENTILITER='cl'
    LITER='l'
    UNIT_CHOICES = (
        (GRAMS, 'Grams'),
        (KILOGRAMS, 'Kilograms'),
        (CENTILITER, 'Centiliter'),
        (LITER, 'Liter')
    )
    #------------------
    unit = models.CharField(
        max_length=2,
        choices=UNIT_CHOICES,
        default=GRAMS,
    )

class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    ingredients = models.ManyToManyField(Ingredient, through='Recipe_Ingredients')

class Recipe_Ingredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()
