from django.forms import ModelForm, TextInput, Textarea, Select
from .models import Category
from recipes.models import Recipe

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name' : TextInput(
                attrs={"placeholder" : "Category Name Here"}
            )
        }
        
        
class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'ingredients', 'directions', 'category', 'image']
        labels = {
            'name': 'Title',
        
        }
        widgets = {
            'name' : TextInput(attrs={'class':'form-control', 'placeholder':'Recipe Title'}),
            'description' : Textarea(attrs={'class':'form-control', 'placeholder':'Description', 'rows':'5'}),
            'ingredients' : Textarea(attrs={'class':'form-control', 'placeholder':'Ingredients', 'rows':'5'}),
            'category' : Select(attrs={'class':'form-select'})
        }