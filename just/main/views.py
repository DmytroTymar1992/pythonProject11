from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from .forms import EmployerLoginForm, SeekerLoginForm

def employer_login_view(request):
    next_url = request.POST.get('next', '/')
    if request.method == 'POST':
        form = EmployerLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect(next_url)  # Перенаправлення на попередню сторінку
    else:
        form = EmployerLoginForm()
    return render(request, 'main/employer_login.html', {'form': form, 'next': next_url})

def seeker_login_view(request):
    next_url = request.POST.get('next', '/')
    if request.method == 'POST':
        form = SeekerLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect(next_url)  # Перенаправлення на попередню сторінку
    else:
        form = SeekerLoginForm()
    return render(request, 'main/seeker_login.html', {'form': form, 'next': next_url})



