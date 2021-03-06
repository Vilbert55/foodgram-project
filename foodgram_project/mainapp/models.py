from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(max_length=100)
    dimension = models.CharField(max_length=30)
    description = models.TextField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title


class Recipe(models.Model):

    title = models.CharField(max_length=50, db_index=True)
    description = models.TextField(max_length=1000)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes')

    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        through='RecipeIngredient')
    image = models.ImageField(upload_to='mainapp/', blank=True, null=True)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    cooking_time = models.PositiveIntegerField(default=1, help_text='(минут)')

    breakfest = models.BooleanField(default=False, verbose_name='Завтрак')
    lunch = models.BooleanField(default=False, verbose_name='Обед')
    dinner = models.BooleanField(default=False, verbose_name='Ужин')

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipe')
    qty = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.ingredient} {self.qty} {self.ingredient.dimension}'


class Purchase(models.Model):
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='purchases')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='purchases')

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['buyer', 'recipe'], name='unique purchase')]


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorites')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorites')

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipe'], name='unique favorite')]


class Follow(models.Model):
    consumer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='consumer')
    cook = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='cook')

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['consumer', 'cook'], name='unique following')]
