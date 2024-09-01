from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from .forms import EmployerLoginForm, SeekerLoginForm
from django.db.models import Count
from company.models import Vacancy, Company
from searcher.forms import VacancySearchForm
from django.core.paginator import Paginator

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


def home(request):
    vacancies_count_all = Vacancy.objects.filter(status__in=['standard', 'standard_plus', 'hot']).count()
    company_count_all = Company.objects.all().count()

    position_counts = Vacancy.objects.filter(
        status__in=['standard', 'standard_plus', 'hot']
    ).values('position__name').annotate(
        count=Count('position')
    ).order_by('-count')[:6]


    category_counts = Vacancy.objects.filter(
        status__in=['standard', 'standard_plus', 'hot']
    ).values('position__categories__id', 'position__categories__name').annotate(
        count=Count('position__categories')
    ).order_by('-count')[:6]

    form = VacancySearchForm()

    context = {
        'vacancies_count_all': vacancies_count_all,
        'company_count_all': company_count_all,
        'position_counts': position_counts,  # Передаємо лише 6 позицій
        'category_counts': category_counts,

        'form': form,
    }

    return render(request, 'main/home.html', context)
