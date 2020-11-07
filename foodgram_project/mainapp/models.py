from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(max_length=50)
    dimension = models.CharField(max_length=4)
    description = models.TextField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title



class Recipe(models.Model):

    title = models.CharField(max_length=50, db_index=True)
    description = models.TextField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes_author')
    
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes_ingredient', through='RecipeIngredient')
    image = models.ImageField(upload_to='mainapp/', blank=True, null=True)
    pub_date = models.DateTimeField('date published', auto_now_add=True)    
    cooking_time = models.PositiveIntegerField(default=1)

    breakfest = models.BooleanField(default=False, verbose_name='Завтрак')
    lunch = models.BooleanField(default=False, verbose_name='Обед')
    dinner = models.BooleanField(default=False, verbose_name='Ужин')

    def __str__(self):
        return self.title

class RecipeIngredient(models.Model):    
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='recipes')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    qty = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.ingredient} {self.qty} {self.ingredient.dimension}'


class Purchase(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='purchases')


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorites')


class Follow(models.Model):
    consumer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consumer')
    cook = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cook')
