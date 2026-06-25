from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomerRegistrationForm, CustomerLoginForm, CustomerProfileForm


def register(request):
    """Handle new customer registration."""
    if request.user.is_authenticated:
        return redirect('menu:menu_home')

    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome! Your account has been created successfully.')
            return redirect('menu:menu_home')
    else:
        form = CustomerRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """Handle customer login using username and password."""
    if request.user.is_authenticated:
        return redirect('menu:menu_home')

    if request.method == 'POST':
        form = CustomerLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You have logged in successfully.')
            return redirect(request.GET.get('next', 'menu:menu_home'))
    else:
        form = CustomerLoginForm(request)

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Handle customer logout via POST request."""
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')


@login_required
def profile(request):
    """Display and update the customer profile."""
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('accounts:profile')
    else:
        form = CustomerProfileForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'form': form})