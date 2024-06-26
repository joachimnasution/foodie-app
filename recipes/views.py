from django.shortcuts import get_object_or_404, render, redirect

from foodie_app.forms import RecipeForm
from recipes.serializer import RecipeSerializer
from .models import Recipe
from comments.forms import CommentForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from rest_framework import viewsets

# Create your views here.
def index(request):
    
    recipes = Recipe.objects.all().values().order_by("-date_added")
    context = {'recipes': recipes}
    
    return render(request, 'recipes/recipes.html', context=context)

def recipe_detail(request, recipe_id):
    # recipe = Recipe.objects.get(id=recipe_id)
    recipe = get_object_or_404(Recipe, id=recipe_id)
    comments = recipe.comments.all()
    
    new_comment = None
    
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            
            new_comment.recipe = recipe
            new_comment.user = request.user
            new_comment.save()
            return redirect(recipe.get_absolute_url())
    else:
        comment_form = CommentForm()
    
    context = {'recipe': recipe, 'comments': comments, 'comment_form': comment_form}
    return render(request, 'recipes/recipe.html', context=context)

def search_results(request):
    query = request.GET.get('search', None)
    unique_results = []
    if query:
        results = Recipe.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(ingredients__icontains=query) | 
            Q(directions__icontains=query) |
            Q(category__name__icontains=query)
            )
        seen_id = set()
        for result in results:
            if result.id not in seen_id:
                seen_id.add(result.id)
                unique_results.append(result)
        
    
    
    context = {'results': unique_results, 'query': query}
    
    return render(request, 'recipes/search_results.html', context=context)
    
@login_required
def toogle_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    if request.user in recipe.favorited_by.all():
        recipe.favorited_by.remove(request.user)
    else:
        recipe.favorited_by.add(request.user)
    
    return redirect('recipes:recipe_detail', recipe_id=recipe_id)

@login_required
def favorite_recipes(request):
    user = request.user
    favorites = user.favorite_recipes.all()
    
    return render(request, 'recipes/favorite_recipes.html', context={'favorites': favorites})

@login_required
def delete_recipes(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    if not request.user == recipe.user and not request.user.is_superuser:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        recipe.delete()
        return redirect('recipes:index')
    
    return render(request, 'recipes/recipe_confirmation_delete.html', context={'recipe': recipe})

@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    if not request.user == recipe.user and not request.user.is_superuser:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        
        if form.is_valid():
            recipe = form.save()
            return redirect('recipes:recipe_detail', recipe_id=recipe_id)
    else:
        form = RecipeForm(instance=recipe)
        
    return render(request, 'recipes/edit_recipe.html', context={'recipe': recipe, 'form': form})


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)