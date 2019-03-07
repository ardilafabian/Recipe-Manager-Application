from django.db import models

class Ingredient(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    cost = models.FloatField()
    amount = models.FloatField()
    #-Unit Choices----
    GRAMS='g.'
    KILOGRAMS='Kg.'
    CENTILITERS='cl.'
    LITERS='l.'
    UNIT_CHOICES = (
        (GRAMS, 'Gram'),
        (KILOGRAMS, 'Kilogram'),
        (CENTILITERS, 'Centiliter'),
        (LITERS, 'Liter')
    )
    #------------------
    unit = models.CharField(
        max_length=2,
        choices=UNIT_CHOICES,
        default=GRAMS,
    )

    def __str__(self):
        return self.name

class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    ingredients = models.ManyToManyField(Ingredient, through='Recipe_Ingredients')

    def __str__(self):
        return self.name

class Recipe_Ingredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()

    def __str__(self):
        r = "{" + str(self.recipe.id)+"|"+self.recipe.name+","+str(self.ingredient.id)+"|"+self.ingredient.name+", quantity:"+str(self.quantity) +"}"
        return r
