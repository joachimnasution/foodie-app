from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import UserProfileForm

# Create your views here.

def register(request):
    
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()            
            login(request, new_user)
            return redirect('foodie_app:index')
        
    context = {'form': form}
    return render(request, 'registration/register.html', context=context)

def edit_user_profile(request):
    if request.method == "POST":
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('foodie_app:index')
    else:
        form = UserProfileForm(instance=request.user.profile)    
    
    return render(request, 'registration/edit_profile.html', context={'form': form})