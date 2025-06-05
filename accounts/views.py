from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
             # Automatically log in the user after registration
            return redirect('accounts:login')  # Redirect to home or any other page
    else:
        form = RegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})

# Create your views here.
