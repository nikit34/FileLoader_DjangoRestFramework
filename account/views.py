from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AuthenticationForm, UpdateForm

from docs.models import Doc


def registation(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        form.save()
        email = form.cleaned_data.get('email').lower()
        password = form.cleaned_data.get('password1')
        account = authenticate(email=email, password=password)
        login(request, account)
        return redirect('home')
    context = {
        'registration_form': form
    }
    return render(request, 'account/register.html', context)


def logout(request):
    logout(request)
    return redirect('home')


def login(request):
    if request.user.is_authenticated:
        return render('home')

    form = AuthenticationForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email').lower()
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            return redirect('home')
    context = {
        'login_form': form
    }
    return render(request, 'account/login.html', context)

def account(request):
    if not request.user.is_authenticated:
        return render('login')

    if request.method == 'POST':
        form = UpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                "email": request.POST['email'],
                "username": request.POST['username'],
            }
            form.save()
    else:
        form = UpdateForm(initial={
            'email': request.user.email,
            'username': request.user.username
        })

    docs = Doc.objects.filter(author=request.user)
    context = {
        'form': form,
        'docs': docs
    }

    return render(request, 'account/account.html', context)


def point_auth(request):
    return render(request, 'account/point_auth.html', {})