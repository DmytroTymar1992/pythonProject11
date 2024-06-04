from django.shortcuts import render, redirect
from .forms import EmailVerificationForm, EmployerRegistrationForm, EmailConfirmationCodeForm, UserProfileForm
from django.contrib.auth import login
import logging
from company.models import Vacancy
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




def edit_profile(request):
    user = request.user
    if user.role != 'employer':
        return redirect('home')  # або інша сторінка, якщо користувач не пошуковець

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            if 'delete_avatar' in request.POST:
                user.avatar.delete(save=True)
            else:
                if 'avatar' in request.FILES:
                    user.avatar = request.FILES['avatar']
            form.save()
            return redirect('edit_profile')  # Перенаправлення на сторінку профілю після збереження
        else:
            # Збереження помилок у сесії
            request.session['form_errors'] = form.errors.as_json()
            return redirect('error_page')  # Перенаправлення на сторінку помилок
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'employer/personal-1.html', {'form': form})


def profile_vacancy_list(request):
    user = request.user
    company = user.company  # Отримуємо компанію, до якої належить користувач
    if company:
        vacancies = Vacancy.objects.filter(company=company)  # Знаходимо вакансії, які належать цій компанії
    else:
        vacancies = Vacancy.objects.none()  # Якщо користувач не належить до компанії, повертаємо пустий QuerySet
    return render(request, 'employer/personal-2.html', {'vacancies': vacancies})
