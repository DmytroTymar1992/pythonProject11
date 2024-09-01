from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import VacancyForm
from .models import JobPosition, JobCategory
from main.models import City
import json
from django.shortcuts import redirect, render
from django.db.models import Q

def position_autocomplete(request):
    if 'term' in request.GET:
        term = request.GET.get('term')
        qs = JobPosition.objects.filter(
            Q(name__icontains=term) | Q(name_ru__icontains=term)
        )[:12]  # Обмеження до 12 записів
        positions = list(qs.values_list('name', 'name_ru'))

        # Форматування результатів для автозаповнення
        results = []
        for job in qs:
            # Спочатку перевіряємо основну назву, інакше додаємо російську назву
            if term.lower() in job.name.lower():
                results.append(job.name)
            elif job.name_ru and term.lower() in job.name_ru.lower():
                results.append(job.name_ru)

        # Видалення дублікатів та обмеження кількості результатів
        unique_results = list(dict.fromkeys(results))[:12]

        return JsonResponse(unique_results, safe=False)

def city_autocomplete(request):
    if 'term' in request.GET:
        qs = City.objects.filter(name__icontains=request.GET.get('term'))
        cities = list(qs.values_list('name', flat=True))
        return JsonResponse(cities, safe=False)


from django.core.exceptions import ValidationError


def create_vacancy(request):
    # Перевіряємо, чи користувач є роботодавцем
    if request.user.role != 'employer':
        return redirect('home')  # Замініть 'home' на вашу URL-ім'я домашньої сторінки

    # Перевіряємо, чи користувач має компанію
    if not request.user.company:
        return redirect('employer_profile')  # Замініть 'profile' на вашу URL-ім'я сторінки профілю

    if request.method == 'POST':
        form = VacancyForm(request.POST)
        if form.is_valid():
            try:
                vacancy = form.save(commit=False)
                vacancy.position = form.cleaned_data['position']
                vacancy.company = request.user.company
                vacancy.save()
                return redirect('success_page')  # Замініть 'success_page' на вашу сторінку успіху
            except Exception as e:
                form.add_error(None, f"Виникла помилка при збереженні вакансії: {str(e)}")
        else:
            form.add_error(None, "Будь ласка, виправте помилки у формі.")
    else:
        form = VacancyForm()

    return render(request, 'company/create-vacancy.html', {'form': form})


def get_categories(request):
    position_name = request.GET.get('position')
    try:
        job_position = JobPosition.objects.get(name=position_name)
        categories = job_position.categories.values('id', 'name')
        return JsonResponse({category['id']: category['name'] for category in categories})
    except JobPosition.DoesNotExist:
        return JsonResponse({"error": "JobPosition not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)