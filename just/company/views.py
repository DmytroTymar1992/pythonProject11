from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import VacancyForm
from .models import JobPosition, JobCategory
import json
from django.shortcuts import redirect, render



def create_vacancy(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        term = request.GET.get('term')
        job_positions = JobPosition.objects.filter(name__icontains=term)
        results = [job.name for job in job_positions]
        return JsonResponse(results, safe=False)

    if request.method == 'POST':
        form = VacancyForm(request.POST)
        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.company = request.user.company  # автоматично встановлюємо компанію
            vacancy.save()
            return redirect('success_url')  # Змінити на URL успішного завершення
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