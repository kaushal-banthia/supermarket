from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

# Create your views here.

def home(request):
    return render(request, 'account/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        # {'name':"rice", 'price':150}
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('account-login')

    else:
        form = UserRegisterForm()
    return render(request, 'account/register.html', {'form': form})

@login_required
def profile(request):
    return render(request,'account/profile.html')


