from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model, decorators
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from .models import Ingredient, Recipe, RecipeIngredient
from .forms import RecipeForm

from django.contrib.auth.decorators import user_passes_test


User = get_user_model()

@user_passes_test(lambda u: u.is_superuser)
def ingredients(request):
    import json
    from django.http import HttpResponse

    with open('ingredients.json', 'r', encoding='utf-8') as fh:
        data = json.load(fh)

    for i in data:
        print('Новый ингридиент:',i)
        ingredient = Ingredient(title=i['title'], dimension=i['dimension'])
        ingredient.save()
    return HttpResponse('\n'.join(str(data)))

def index(request):
    if request.GET.get('filter') == 'breakfest':
        recipe_list = Recipe.objects.filter(breakfest=True).order_by('-pub_date')
    elif request.GET.get('filter') == 'lunch':
        recipe_list = Recipe.objects.filter(lunch=True).order_by('-pub_date')
    elif request.GET.get('filter') == 'dinner':
        recipe_list = Recipe.objects.filter(dinner=True).order_by('-pub_date')
    else:
        recipe_list = Recipe.objects.order_by('-pub_date').all()
    
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    #if request.user.is_authenticated:
    return render(request, 'indexAuth3.html', {'page': page, 'paginator': paginator})
    #return render(request, 'indexNotAuth.html')

def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST or None, files=request.FILES or None, )
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('index')
        return render(request, 'new_recipe.html', {'form':form})
    form = RecipeForm()
    return render(request, 'formRecipe.html', {'form':form})


def recipe_view(request, username, recipe_id):
    author = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, pk=recipe_id, author=author)
    inrgedients = RecipeIngredient.objects.filter(recipe_id=recipe.pk)
    for i in inrgedients:
        WWWWWWWWWWW = 1
        print('WWWWWWWWWWWWWWW', i.ingredient)
    return render(request, 'singlePage.html', {'recipe':recipe, 'username':author, 'inrgedients':inrgedients})