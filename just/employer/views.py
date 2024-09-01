import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import EmailVerificationForm, EmployerRegistrationForm, EmailConfirmationCodeForm, UserProfileForm
from django.contrib.auth import login
import logging
from company.models import Vacancy
from django.contrib import messages
from main.models import User, City
from django.db.models import Count
from django.core.paginator import Paginator

logger = logging.getLogger(__name__)


def register_employer_step1(request):
    if request.method == 'POST':
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            request.session['email'] = form.cleaned_data['email']
            return redirect('register_employer_step2')
        else:
            messages.error(request, 'Цей email вже зареєстрований.')
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
            city_name = form.cleaned_data.get('city_name')
            try:
                city = City.objects.get(name__iexact=city_name)
                user.city = city
                user.save()
                login(request, user, backend='main.backends.EmployerAuthBackend')
                return redirect('main-employer-no-auth')
            except City.DoesNotExist:
                messages.error(request, 'Невірне місто.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if error == 'Invalid city name.':
                        messages.error(request, 'Невірне місто.')
                    elif error == 'This field is required.':
                        messages.error(request, 'Це поле є обов\'язковим.')
                    else:
                        messages.error(request, error)
    else:
        form = EmployerRegistrationForm(initial={'email': request.session.get('email')})
    return render(request, 'employer/registration-step-3.html', {'form': form})

def registration_error(request):
    return render(request, 'employer/registration-error.html')




@login_required
def edit_profile(request):
    user = request.user
    if user.role != 'employer':
        return redirect('home')  # або інша сторінка, якщо користувач не роботодавець

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            if 'delete_avatar' in request.POST:
                user.avatar.delete(save=True)
                messages.success(request, 'Аватар видалено.')

            city_name = form.cleaned_data.get('city_name')
            try:
                city = City.objects.get(name__iexact=city_name)
                user.city = city
                form.save(commit=False)
                user.save()
                messages.success(request, 'Профіль оновлено.')
                return redirect('employer_profile')
            except City.DoesNotExist:
                messages.error(request, 'Невірне місто.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if error == 'Invalid city name.':
                        messages.error(request, 'Невірне місто.')
                    elif error == 'This field is required.':
                        messages.error(request, f'{field}: Це поле є обов\'язковим.')
                    elif error == 'User with this Phone already exists.':
                        messages.error(request, 'Користувач з таким номером вже зареєстрований')
                    elif error == 'User with this Email already exists.':
                        messages.error(request, 'Користувач з таким Email вже зареєстрований')
                    elif error == 'invalid_format':
                        messages.error(request, 'Не вірний номер')
                    else:
                        messages.error(request, f'{field}: {error}')
    else:
        initial_data = {'city_name': user.city.name if user.city else ''}
        form = UserProfileForm(instance=user, initial=initial_data)

    return render(request, 'employer/personal-1.html', {'form': form})


def profile_vacancy_list(request):
    user = request.user
    company = user.company
    status = request.GET.get('status', 'active')


    if company:
        active_vacancies = Vacancy.objects.filter(company=company, status__in=['standard', 'standard_plus', 'hot']).order_by('-publication_date')
        closed_vacancies = Vacancy.objects.filter(company=company, status__in=['hidden'])

        active_vacancies = active_vacancies.annotate(feedback_count=Count('feedback'))
        closed_vacancies = closed_vacancies.annotate(feedback_count=Count('feedback'))

        if status == 'active':
            vacancies = active_vacancies
        elif status == 'closed':
            vacancies = closed_vacancies

        active_vacancies_count = active_vacancies.count()
        closed_vacancies_count = closed_vacancies.count()

        paginator = Paginator(vacancies, 6)
        page_number = request.GET.get('page', 1)
        vacancies = paginator.get_page(page_number)  # Отримуємо вакансії для поточної сторінки

        current_page = vacancies.number
        total_pages = vacancies.paginator.num_pages

        start_page = max(current_page - 3, 2)
        end_page = min(current_page + 3, total_pages - 1)

        pages = range(start_page, end_page + 1)

        show_first_dots = pages[0] > 2
        show_last_dots = pages[-1] < total_pages - 1

    else:
        vacancies = Vacancy.objects.none()
        active_vacancies_count = 0
        closed_vacancies_count = 0
        pages = []

    return render(request, 'employer/personal-2.html', {
        'vacancies': vacancies,
        'active_vacancies_count': active_vacancies_count,
        'closed_vacancies_count': closed_vacancies_count,
        'status': status,
        'pages': pages,
        'total_pages': total_pages,
        'show_first_dots': show_first_dots,
        'show_last_dots': show_last_dots,
    })