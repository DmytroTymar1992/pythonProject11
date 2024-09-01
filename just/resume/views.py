import logging
from django.shortcuts import render, redirect
from .forms import (
                    ResumeForm,
                    EducationFormSet,
                    WorkExperienceFormSet,
                    CourseFormSet,
                    UserLanguageFormSet,
                    )
from company.models import JobPosition
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required
def create_resume(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        term = request.GET.get('term', '')
        job_positions = JobPosition.objects.filter(name__icontains=term)[:10]
        results = [job.name for job in job_positions]
        return JsonResponse(results, safe=False)

    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES, user=request.user)
        education_formset = EducationFormSet(request.POST, request.FILES)
        work_experience_formset = WorkExperienceFormSet(request.POST, request.FILES)
        course_formset = CourseFormSet(request.POST, request.FILES)
        user_language_formset = UserLanguageFormSet(request.POST, request.FILES)

        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()

            education_formset.instance = resume
            work_experience_formset.instance = resume
            course_formset.instance = resume
            user_language_formset.instance = resume



            formset_errors = {}

            if education_formset.is_valid() and work_experience_formset.is_valid() and course_formset.is_valid() and user_language_formset.is_valid():
                form.save_m2m()
                education_formset.save()
                work_experience_formset.save()
                course_formset.save()
                user_language_formset.save()
                return redirect('resume_detail', pk=resume.pk)
            else:
                if not education_formset.is_valid():
                    formset_errors['education_formset'] = education_formset.errors
                if not work_experience_formset.is_valid():
                    formset_errors['work_experience_formset'] = work_experience_formset.errors
                if not course_formset.is_valid():
                    formset_errors['course_formset'] = course_formset.errors
                if not user_language_formset.is_valid():
                    formset_errors['user_language_formset'] = user_language_formset.errors

                return render(request, 'resume/create-resume.html', {
                    'form': form,
                    'education_formset': education_formset,
                    'work_experience_formset': work_experience_formset,
                    'course_formset': course_formset,
                    'user_language_formset': user_language_formset,
                    'errors': form.errors,
                    'formset_errors': formset_errors,
                })
        else:
            return render(request, 'resume/create-resume.html', {
                'form': form,
                'education_formset': education_formset,
                'work_experience_formset': work_experience_formset,
                'course_formset': course_formset,
                'user_language_formset': user_language_formset,
                'errors': form.errors,
            })
    else:
        form = ResumeForm(user=request.user)
        education_formset = EducationFormSet()
        work_experience_formset = WorkExperienceFormSet()
        course_formset = CourseFormSet()
        user_language_formset = UserLanguageFormSet()

    return render(request, 'resume/create-resume.html', {
        'form': form,
        'education_formset': education_formset,
        'work_experience_formset': work_experience_formset,
        'course_formset': course_formset,
        'user_language_formset': user_language_formset,
    })
