from django.views.decorators.csrf import csrf_exempt
import logging
from django.shortcuts import render, redirect, get_object_or_404
from .forms import (PhoneVerificationForm,
                    SeekerRegistrationForm,
                    ConfirmationCodeForm,
                    UserProfileForm,
                    VacancySearchForm,

                    )
from django.views import View
from django.contrib.auth import login
from main.models import User, City
from django.contrib.auth.decorators import login_required
from .models import SavedVacancy
from django.http import JsonResponse
from company.models import JobPosition, Vacancy, JobPositionGroup, JobCategory
from feedback.models import Feedback
import json
from django.db.models import Q, Case, When, Value, IntegerField
from django.contrib import messages
from django.utils.timesince import timesince
from django.utils import timezone
from django.utils.translation import gettext as _
from resume.models import Resume
from django.db.models import Count

logger = logging.getLogger(__name__)

def register_seeker_step1(request):
    if request.method == 'POST':
        form = PhoneVerificationForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            if User.objects.filter(phone=phone).exists():
                messages.error(request, 'Цей номер телефону вже зареєстрований. Будь ласка, увійдіть в акаунт.')
            else:
                request.session['phone'] = phone
                return redirect('register_seeker_step2')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if error == 'invalid_format':
                        messages.error(request, 'Неправильний формат номера телефону.')
                    elif error == 'This field is required.':
                        messages.error(request, 'Це поле є обовязковим.')
                    else:
                        messages.error(request, error)
    else:
        form = PhoneVerificationForm()
    return render(request, 'searcher/registration-step-1.html', {'form': form})


def register_seeker_step2(request):
    if request.method == 'POST':
        form = ConfirmationCodeForm(request.POST)
        if form.is_valid():
            return redirect('register_seeker_step3')
    else:
        form = ConfirmationCodeForm()
    return render(request, 'searcher/registration-step-2.html', {'form': form})

def register_seeker_step3(request):
    if request.method == 'POST':
        form = SeekerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'seeker'
            user.phone = request.session.get('phone')
            city_name = form.cleaned_data.get('city_name')
            try:
                city = City.objects.get(name__iexact=city_name)
                user.city = city
                user.save()
                login(request, user, backend='main.backends.SeekerAuthBackend')
                return redirect('home')
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
        form = SeekerRegistrationForm(initial={'phone': request.session.get('phone')})
    return render(request, 'searcher/registration-step-3.html', {'form': form})





def get_city_id(request):
    city_name = request.GET.get('city_name')
    try:
        city = City.objects.get(name=city_name)
        return JsonResponse({'city_id': city.id})
    except City.DoesNotExist:
        return JsonResponse({'city_id': None})


def get_city_suggestions(request):
    term = request.GET.get('term', '').strip()
    cities = City.objects.filter(name__icontains=term)  # Використовуємо icontains для нечутливого до регістру пошуку
    results = [{'name': city.name, 'id': city.id} for city in cities]
    return JsonResponse(results, safe=False)





@login_required
def edit_profile(request):
    user = request.user
    if user.role != 'seeker':
        return redirect('home')  # або інша сторінка, якщо користувач не пошуковець

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
                return redirect('edit_profile')
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
        initial_data = {'city_name': user.city.name if user.city else '2'}
        form = UserProfileForm(instance=user, initial=initial_data)

    return render(request, 'searcher/personal-1.html', {'form': form})


@login_required
def error_page(request):
    errors = request.session.get('form_errors', '{}')
    errors = json.loads(errors, cls=json.JSONDecoder)
    return render(request, 'searcher/resume_error_page.html', {'errors': errors})


@login_required
def profile_resume_list(request):
    user = request.user
    resumes = Resume.objects.filter(user=user)
    resume_list = [
        {
            'resume': resume,
            'pk': resume.pk,
            'time_since_modified': translate_timesince(timesince(resume.date_modified, timezone.now()))
        }
        for resume in resumes
    ]
    return render(request, 'searcher/personal-2.html', {'resume_list': resume_list})


@login_required
def delete_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    resume.delete()
    return redirect('profile_resume_list')


@login_required
def resume_detail(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    return render(request, 'searcher/resume-details.html', {'resume': resume})


def translate_timesince(timesince_string):
    translations = {
        'minute': _('хвилина'),
        'minutes': _('хвилин'),
        'hour': _('година'),
        'hours': _('годин'),
        'day': _('день'),
        'days': _('днів'),
        'week': _('тиждень'),
        'weeks': _('тижнів'),
        'month': _('місяць'),
        'months': _('місяців'),
        'year': _('рік'),
        'years': _('років')
    }
    for en, uk in translations.items():
        timesince_string = timesince_string.replace(en, uk)
    return timesince_string


def vacancy_list(request):
    form = VacancySearchForm(request.GET)
    vacancies = Vacancy.objects.filter(~Q(status='hidden')).annotate(
        is_hot=Case(
            When(status='hot', then=Value(0)),
            default=Value(1),
            output_field=IntegerField(),
        )
    ).order_by('is_hot', '-publication_date')

    category_id = request.GET.get('category')  # Отримуємо ID вибраної категорії

    if category_id:
        vacancies = vacancies.filter(position__categories__id=category_id)

    if form.is_valid():
        title = form.cleaned_data.get('title')
        city = form.cleaned_data.get('city')

        if title:
            # Знайти посади, які відповідають введеній назві
            positions = JobPosition.objects.filter(Q(name__icontains=title) | Q(name_ru__icontains=title))
            if positions.exists():
                # Знайти групи цих посад
                groups = JobPositionGroup.objects.filter(job_positions_by_group__in=positions).distinct()
                # Знайти всі посади, які належать до цих груп
                group_positions = JobPosition.objects.filter(groups__in=groups).distinct()
                # Знайти вакансії, які відповідають цим посадам
                vacancies = vacancies.filter(position__in=group_positions)

        if city:
            vacancies = vacancies.filter(Q(city__name__icontains=city) | Q(city__name_ru__icontains=city))

    if request.user.is_authenticated:
        saved_vacancies = SavedVacancy.objects.filter(user=request.user).values_list('vacancy_id', flat=True)
        saved_vacancies_ids = list(saved_vacancies)
    else:
        saved_vacancies_ids = []

    if request.user.is_authenticated:
        feedback_vacancies = Feedback.objects.filter(job_seeker=request.user).values_list('vacancy_id', flat=True)
        feedback_vacancies_ids = list(feedback_vacancies)
    else:
        feedback_vacancies_ids = []

    categories = Vacancy.objects.filter(
        status__in=['standard', 'standard_plus', 'hot']
    ).values('position__categories__id', 'position__categories__name').annotate(
        count=Count('position__categories')
    )

    context = {
        'form': form,
        'vacancies': vacancies,
        'saved_vacancies_ids': saved_vacancies_ids,
        'categories': categories,
        'feedback_vacancies_ids': feedback_vacancies_ids
    }
    return render(request, 'searcher/vacancies-page.html', context)


def vacancy_detail(request, slug, vacancy_id):
    vacancy = get_object_or_404(Vacancy, id=vacancy_id, position__slug=slug)

    if not request.user.is_authenticated or request.user.role == 'seeker':
        vacancy.view_count += 1
        vacancy.save()

    context = {
        'vacancy': vacancy
    }
    return render(request, 'searcher/vacancies-item.html', context)


@login_required
def delete_saved_vacancy(request, vacancy_id):
    if request.method == 'GET':
        saved_vacancy = get_object_or_404(SavedVacancy, user=request.user, vacancy_id=vacancy_id)
        saved_vacancy.delete()
        messages.success(request, 'Вакансію видалено із збережених.')
        return redirect('profile_resume_saved_vacancies')
    return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt
def toggle_save_vacancy(request, vacancy_id):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'Увійдіть, щоб мати можливість зберігати вакансії.'},
                                status=403)

            # Перевірка ролі користувача
        if request.user.role == 'employer':  # Припускаємо, що роль користувача зберігається в атрибуті `role`
            return JsonResponse({'status': 'error',
                                 'message': 'Роботодавці не мають можливості зберігати вакансії, увійдіть як пошуковець.'},
                                status=403)
        vacancy = get_object_or_404(Vacancy, id=vacancy_id)
        saved_vacancy, created = SavedVacancy.objects.get_or_create(user=request.user, vacancy=vacancy)
        if not created:
            saved_vacancy.delete()
            return JsonResponse({'status': 'deleted'})
        return JsonResponse({'status': 'saved'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def profile_resume_saved_vacancies(request):
    saved_vacancies = SavedVacancy.objects.filter(user=request.user).select_related('vacancy')
    context = {
        'saved_vacancies': saved_vacancies,
    }
    return render(request, 'searcher/personal-4.html', context)