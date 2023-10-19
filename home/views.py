from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import SignUpForm
from django.shortcuts import render, redirect 
from django.urls import reverse
# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('ads:ad_list'))  # Replace 'home' with the name of your homepage URL pattern
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})