from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import VacancyForm
from .models import JobPosition

def create_vacancy(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        term = request.GET.get('term')
        job_positions = JobPosition.objects.filter(name__icontains=term)
        results = [job.name for job in job_positions]
        return JsonResponse(results, safe=False)

    if request.method == 'POST':
        form = VacancyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # замінити на актуальний URL списку вакансій
    else:
        form = VacancyForm()
    return render(request, 'company/create-vacancy.html', {'form': form})
