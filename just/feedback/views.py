from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Feedback
from company.models import Vacancy, Company
from resume.models import Resume
import json
from django.http import JsonResponse
from .models import Feedback
from datetime import date
from django.template.loader import render_to_string
from django.middleware.csrf import get_token
from django.db.models import Count
from .forms import *
from main.models import User
from django.contrib.auth.models import AnonymousUser

def save_feedback(request, vacancy_id):
    if request.method == 'POST':
        vacancy = get_object_or_404(Vacancy, id=vacancy_id)

        # Перевірка авторизації користувача
        if isinstance(request.user, AnonymousUser):
            return JsonResponse({'status': 'lead'})

        # Перевіряємо, чи користувач уже створив відгук для цієї вакансії
        existing_feedback = Feedback.objects.filter(vacancy=vacancy, job_seeker=request.user).exists()
        if existing_feedback:
            return JsonResponse({'status': 'error', 'message': 'Ви вже відгукнулись на цю вакансію.'}, status=403)

        resumes = request.user.resumes.all()

        if resumes.count() > 1 and 'resume_id' not in request.POST:
            # Якщо більше одного резюме і користувач ще не вибрав резюме, повертаємо їх список для вибору в модальному вікні
            return JsonResponse(
                {'status': 'select_resume', 'resumes': [{'id': resume.id, 'name': resume.positions} for resume in resumes]}
            )

        # Обробка вибору резюме
        selected_resume_id = request.POST.get('resume_id')
        if selected_resume_id:
            try:
                resume = request.user.resumes.get(id=selected_resume_id)
            except Resume.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Обране резюме не існує.'}, status=400)
        else:
            resume = request.user.resumes.first()

        # Створюємо новий відгук
        feedback = Feedback(
            vacancy=vacancy,
            job_seeker=request.user,
            resume=resume  # Використовуємо вибране резюме або перше, якщо користувач не вибрав резюме
        )
        feedback.save()

        return JsonResponse({'status': 'success', 'message': 'Ваш відгук було успішно додано.'})

    return JsonResponse({'status': 'error'}, status=400)


def save_lead_feedback(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)

    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            name = form.cleaned_data['name']

            # Зберігаємо дані в сесії
            request.session['lead_phone'] = phone
            request.session['lead_name'] = name

            # Перевіряємо, чи є номер телефону серед існуючих лідів або користувачів
            existing_lead = Lead.objects.filter(phone=phone).first()
            existing_user = User.objects.filter(phone=phone).first()

            if existing_user:
                return JsonResponse({'status': 'error', 'message': 'Такий номер зареєстрований, увійдіть в свій акаунт.'}, status=400)

            if existing_lead:
                existing_feedback = Feedback.objects.filter(vacancy=vacancy, lead=existing_lead).exists()
                if existing_feedback:
                    return JsonResponse({'status': 'error', 'message': 'Ви вже відгукнулись на цю вакансію.'}, status=400)
                else:
                    lead = existing_lead
            else:
                # Створюємо нового ліда
                lead = form.save()

            # Створюємо новий відгук
            feedback = Feedback(
                vacancy=vacancy,
                lead=lead,
                status='new',
            )
            feedback.save()

            return JsonResponse({'status': 'success', 'message': 'Ваш відгук було успішно додано.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Форма не є валідною.'}, status=400)

    return JsonResponse({'status': 'error'}, status=400)


def employer_feedback_list(request):
    if request.user.is_authenticated and request.user.role == 'employer':
        company = request.user.company

        if not company:
            return render(request, 'feedback/personal-3.html', {'feedbacks': [], 'status_counts': {}})

        vacancies = Vacancy.objects.filter(company=company)
        feedbacks = Feedback.objects.filter(vacancy__in=vacancies).order_by('-created_at')

        # Підрахунок кількості відгуків за статусами
        status_counts = feedbacks.values('status').annotate(count=Count('status')).order_by()

        # Створення словника для зберігання підрахунків
        status_counts_dict = {status['status']: status['count'] for status in status_counts}
        # Додавання загального підрахунку для "Всі"
        status_counts_dict['all'] = feedbacks.count()

        selected_vacancy_id = request.GET.get('vacancy')
        if selected_vacancy_id and selected_vacancy_id != 'all':
            feedbacks = feedbacks.filter(vacancy_id=selected_vacancy_id)
            status_counts = feedbacks.values('status').annotate(count=Count('status')).order_by()
            status_counts_dict = {status['status']: status['count'] for status in status_counts}
            status_counts_dict['all'] = feedbacks.count()

        selected_status = request.GET.get('status')
        if selected_status and selected_status != 'all':
            feedbacks = feedbacks.filter(status=selected_status)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            csrf_token = get_token(request)
            html = render_to_string('feedback/feedback_list.html', {'feedbacks': feedbacks})
            return JsonResponse({'html': html, 'csrf_token': csrf_token, 'status_counts': status_counts_dict})

        context = {
            'feedbacks': feedbacks,
            'vacancies': vacancies,
            'status_counts': status_counts_dict,
        }
        return render(request, 'feedback/personal-3.html', context)
    else:
        return render(request, 'feedback/personal-3.html', {'feedbacks': [], 'status_counts': {}})



@login_required
def update_feedback_status(request, feedback_id):
    if request.method == 'POST':
        feedback = get_object_or_404(Feedback, id=feedback_id)

        # Переконайтеся, що користувач пов'язаний з компанією, якій належить вакансія
        if request.user.role != 'employer' or feedback.vacancy.company != request.user.company:
            return JsonResponse({'status': 'error', 'message': 'Ви не маєте прав для зміни статусу цього відгуку.'}, status=403)

        new_status = request.POST.get('status')
        if new_status in dict(Feedback.STATUS_CHOICES).keys():
            feedback.status = new_status
            feedback.save()
            return JsonResponse({'status': 'success', 'message': 'Статус відгуку змінено успішно.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Невірний статус.'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Невірний запит.'}, status=400)