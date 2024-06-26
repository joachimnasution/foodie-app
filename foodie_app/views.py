from django.shortcuts import render, redirect, get_object_or_404
from .models import Category
from recipes.models import Recipe
from .forms import CategoryForm, RecipeForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    
    categories = Category.objects.all()
    context = {'categories': categories}
    
    return render(request, "foodie_app/index.html", context=context)

def recipe(request, category_id):
    recipes = Recipe.objects.filter(category_id=category_id).order_by("-date_added")
    category = Category.objects.get(id=category_id)
    
    context = {'recipes': recipes, 'category': category}
    
    return render(request, "foodie_app/recipes.html", context=context)

@login_required
def add_category(request):
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('foodie_app:index')
        else:
            context = {'form': form}
            return render(request, "foodie_app/add_category.html", context=context)
    
    form = CategoryForm()
    context = {'form': form}
    return render(request, "foodie_app/add_category.html", context=context)

@login_required
def add_recipe(request, category_id=None):
    category_id = category_id
    initial_data = {}
    
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        initial_data = {'category': category}

    if request.method == 'POST':
        print('Trying to save')
        form = RecipeForm(request.POST, request.FILES, initial=initial_data)
        if form.is_valid():
            new_recipe = form.save(commit=False)
            new_recipe.user = request.user
            new_recipe.save()
            return redirect('foodie_app:recipes', category_id=new_recipe.category.id)
    else:
        form = RecipeForm(initial=initial_data)
            
    context = {'form': form, 'category':category_id}
    return render(request, "foodie_app/add_recipe.html", context=context)