from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(max_length=50)
    dimension = models.CharField(max_length=4)
    description = models.TextField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):    
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='ingredient_for_recipes')
    qty = models.PositiveIntegerField(default=1)

    def __str__(self):
        return 'Ингредиент: {} (для рецепта)'.format(self.ingredient)


class Recipe(models.Model):
    #BREAKFEST = 'Завтрак'
    #LUNCH = 'Обед'
    #DINNER = 'Ужин'

    #FOOD_TIME = [
    #    (BREAKFEST, 'Завтрак'),
    #    (LUNCH, 'Обед'),
    #    (DINNER, 'Ужин'),
    #]

    title = models.CharField(max_length=50, db_index=True)
    description = models.TextField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes_author')
    owners = models.ManyToManyField(User, related_name='recipes_owner', blank=True)
    ingredients = models.ManyToManyField(RecipeIngredient, related_name='recipes_ingredient')
    image = models.ImageField(upload_to='mainapp/', blank=True, null=True)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    #tag = models.CharField(max_length=20, choices=FOOD_TIME, default=BREAKFEST, many=true)
    cooking_time = models.PositiveIntegerField(default=1)
    breakfest = models.BooleanField(default=False)
    lunch = models.BooleanField(default=False)
    dinner = models.BooleanField(default=False)


    def __str__(self):
        return self.title


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')



