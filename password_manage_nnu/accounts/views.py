from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages

from .forms import RegisterForm, LoginForm
from .models import UserProfile


def home(request):
    """Home page with dynamic user count."""
    user_count = User.objects.count()
    return render(request, 'home.html', {'user_count': user_count})


def about(request):
    """About page."""
    return render(request, 'about.html')


def contact(request):
    """Contact page."""
    return render(request, 'contact.html')


def register_view(request):
    """Handle user registration with passkey creation."""
    if request.user.is_authenticated:
        return redirect('vault_dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            # Hash the passkey using Django's password hashing (PBKDF2)
            UserProfile.objects.create(
                user=user,
                passkey_hash=make_password(form.cleaned_data['passkey']),
            )
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to PassManNNU.')
            return redirect('vault_dashboard')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """Handle user login with basic rate limiting via session."""
    if request.user.is_authenticated:
        return redirect('vault_dashboard')

    # Basic rate limiting
    attempts_key = 'login_attempts'
    lockout_key = 'login_lockout'

    if request.session.get(lockout_key):
        messages.error(request, 'Too many failed login attempts. Please try again later.')
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Reset attempts on success
            request.session.pop(attempts_key, None)
            request.session.pop(lockout_key, None)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('vault_dashboard')
        else:
            attempts = request.session.get(attempts_key, 0) + 1
            request.session[attempts_key] = attempts
            if attempts >= 5:
                request.session[lockout_key] = True
                messages.error(request, 'Too many failed attempts. Account temporarily locked.')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Log out and redirect to home."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')
