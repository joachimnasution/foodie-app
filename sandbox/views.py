from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, View
from recipes.models import Recipe
from sandbox.form import FeedbackForm
from django.http import HttpResponse
from .models import Feedback
from django.contrib import messages



# Create your views here.
def index(request):
    recipes = Recipe.objects.all().order_by('-date_added')
    context = {'recipes': recipes}
    return render(request, 'sandbox/index.html', context=context)


class RecipeListView(ListView):
    model = Recipe
    template_name = 'sandbox/index.html'
    context_object_name = 'recipes'
    ordering = ['date_added']
    
    def get_queryset(self):
        recipe = Recipe.objects.filter(name__icontains='makanan')
        return recipe
    
class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'sandbox/recipe.html'
    context_object_name = 'recipe'
    
class SpecificRecipesView(View):
    
    def get(self, request, *args, **kwargs):
        recipes = Recipe.objects.filter(description__icontains='makanan')
        return render(request, 'sandbox/spesifik.html', context={'recipes': recipes})
    
    
def thank_you(request):
    return HttpResponse('<h1>Thank you for your feedback!</h1>')
    
def feedback_view(request):
    
    request.session['feedback_visits'] = request.session.get('feedback_visits', 0) + 1
    
    # request.session.flush()
    # print("Expireds", request.session.get_expiry_date())
    
    form = FeedbackForm()
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            
            request.session['feedback_data'] = form.cleaned_data
            return redirect('sandbox:feedback_review')
            
            # name = form.cleaned_data['name']
            # email = form.cleaned_data['email']
            # feedback = form.cleaned_data['feedback']
            # satisfaction = form.cleaned_data['satisfaction']
            
            # Feedback.objects.create(name=name, email=email, feedback=feedback, satisfaction=satisfaction)
            # messages.add_message(request, messages.SUCCESS, 'Feedback send successfully!')

            # return redirect('sandbox:index')
    
    context = {'form': form, 'visits': request.session['feedback_visits']}
        
    return render(request, 'sandbox/feedback.html', context=context)


def feedback_review(request):
    feeback_data = request.session.get('feedback_data', {})
    
    if request.method == 'POST': 
        if feeback_data:
            Feedback.objects.create(**feeback_data)
            messages.success(request, 'Feedback send successfully!')
            
            del request.session['feedback_data']
            
            return redirect('sandbox:index')
    
    form = FeedbackForm(initial=feeback_data)
    context = {'form': form}
    return render(request, 'sandbox/feedback_review.html', context=context)