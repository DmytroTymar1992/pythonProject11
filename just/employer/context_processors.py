from company.models import Vacancy, Company
from django.db.models import Count

def vacancies_count(request):
    user = request.user
    if user.is_authenticated:
        company = user.company
        if company:
            vacancies_count = Vacancy.objects.filter(company=company).count()
        else:
            vacancies_count = 0
    else:
        vacancies_count = 0
    return {'vacancies_count': vacancies_count}


