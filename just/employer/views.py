from django.shortcuts import render, redirect
from .forms import EmailVerificationForm, EmployerRegistrationForm, EmailConfirmationCodeForm
from django.contrib.auth import login
import logging

logger = logging.getLogger(__name__)

def register_employer_step1(request):
    if request.method == 'POST':
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            request.session['email'] = form.cleaned_data['email']
            return redirect('register_employer_step2')
    else:
        form = EmailVerificationForm()
    return render(request, 'employer/registration-step-1.html', {'form': form})


def register_employer_step2(request):
    if request.method == 'POST':
        form = EmailConfirmationCodeForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['code'] == '1111':
                return redirect('register_employer_step3')
            else:
                form.add_error('code', 'Неправильний код підтвердження.')
    else:
        form = EmailConfirmationCodeForm()
    return render(request, 'employer/registration-step-2.html', {'form': form})


def register_employer_step3(request):
    if request.method == 'POST':
        form = EmployerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'employer'  # Явно встановлюємо роль роботодавця
            user.email = request.session.get('email')  # Отримуємо email із сесії
            user.save()

            # Логін користувача з використанням бекенду для роботодавців
            login(request, user, backend='main.backends.EmployerAuthBackend')

            return redirect('main-employer-no-auth')
        else:
            # Log form errors
            logger.error("Registration form errors: %s", form.errors)
            return render(request, 'employer/registration-error.html', {'form_errors': form.errors})
    else:
        form = EmployerRegistrationForm(initial={'email': request.session.get('email')})
    return render(request, 'employer/registration-step-3.html', {'form': form})

def registration_error(request):
    return render(request, 'employer/registration-error.html')
