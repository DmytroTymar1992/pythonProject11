import logging
from django.shortcuts import render, redirect, get_object_or_404
from .forms import (PhoneVerificationForm,
                    SeekerRegistrationForm,
                    ConfirmationCodeForm,
                    ResumeForm,
                    EducationFormSet,
                    WorkExperienceFormSet,
                    CourseFormSet,
                    UserLanguageFormSet,
                    UserProfileForm
                    )

from django.contrib.auth import login
from main.models import User
from django.contrib.auth.decorators import login_required
from .models import Resume
from django.http import JsonResponse
from company.models import JobPosition
import json





logger = logging.getLogger(__name__)

def register_seeker_step1(request):
    if request.method == 'POST':
        form = PhoneVerificationForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            if User.objects.filter(phone=phone).exists():
                form.add_error('phone', 'Цей номер телефону вже зареєстрований. Будь ласка, увійдіть в акаунт.')
            else:
                request.session['phone'] = phone
                return redirect('register_seeker_step2')
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
            user.role = 'seeker'  # Явно встановлюємо роль пошуковця
            user.phone = request.session.get('phone')  # Отримуємо номер телефону із сесії
            user.save()

            # Логін користувача з використанням бекенду для пошуковців
            login(request, user, backend='main.backends.SeekerAuthBackend')

            return redirect('home')
        else:
            # Log form errors
            logger.error("Registration form errors: %s", form.errors)
            return render(request, 'searcher/registration-error.html', {'form_errors': form.errors})
    else:
        form = SeekerRegistrationForm(initial={'phone': request.session.get('phone')})
    return render(request, 'searcher/registration-step-3.html', {'form': form})

def registration_error(request):
    return render(request, 'searcher/registration-error.html')


@login_required
def create_resume(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        term = request.GET.get('term', '')
        job_positions = JobPosition.objects.filter(name__icontains=term)[:10]
        results = [job.name for job in job_positions]
        return JsonResponse(results, safe=False)

    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()

            education_formset = EducationFormSet(request.POST, instance=resume)
            work_experience_formset = WorkExperienceFormSet(request.POST, request.FILES, instance=resume)
            course_formset = CourseFormSet(request.POST, instance=resume)
            user_language_formset = UserLanguageFormSet(request.POST, instance=resume)

            if (education_formset.is_valid() and
                    work_experience_formset.is_valid() and
                    course_formset.is_valid() and
                    user_language_formset.is_valid()):

                education_formset.save()
                work_experience_formset.save()
                course_formset.save()
                user_language_formset.save()


                form.save_m2m()


                desired_positions = form.cleaned_data.get('desired_positions')
                if desired_positions:
                    resume.desired_positions.set(desired_positions)

                return redirect('resume_detail', pk=resume.pk)
    else:
        form = ResumeForm(user=request.user)
        education_formset = EducationFormSet(instance=Resume())
        work_experience_formset = WorkExperienceFormSet(instance=Resume())
        course_formset = CourseFormSet(instance=Resume())
        user_language_formset = UserLanguageFormSet(instance=Resume())

    return render(request, 'searcher/create-resume.html', {
        'form': form,
        'education_formset': education_formset,
        'work_experience_formset': work_experience_formset,
        'course_formset': course_formset,
        'user_language_formset': user_language_formset
    })


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
    return render(request, 'searcher/personal-2.html', {'resumes': resumes})