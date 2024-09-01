from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (register_seeker_step1,
                    register_seeker_step2,
                    register_seeker_step3,
                    edit_profile,
                    error_page,
                    vacancy_list,
                    vacancy_detail,
                    #save_vacancy,
                    toggle_save_vacancy,
                    profile_resume_saved_vacancies,
                    get_city_suggestions,
                    delete_saved_vacancy
                    )
from . import views
from django.conf.urls.static import static


urlpatterns = [
    path('register/step1/', register_seeker_step1, name='register_seeker_step1'),
    path('register/step2/', register_seeker_step2, name='register_seeker_step2'),
    path('register/step3/', register_seeker_step3, name='register_seeker_step3'),
    path('get_city_suggestions/', get_city_suggestions, name='get_city_suggestions'),
    path('get_city_id/', views.get_city_id, name='get_city_id'),


    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/edit/error/', error_page, name='error_page'),
    path('profile/resumes/', views.profile_resume_list, name='profile_resume_list'),
    path('vacancies/', vacancy_list, name='vacancy_list'),
    path('vacancy/<slug:slug>/<int:vacancy_id>/', vacancy_detail, name='vacancy_detail'),
    #path('save-vacancy/<int:vacancy_id>/', save_vacancy, name='save_vacancy'),
    path('toggle-save-vacancy/<int:vacancy_id>/', toggle_save_vacancy, name='toggle_save_vacancy'),
    path('delete-saved-vacancy/<int:vacancy_id>/', delete_saved_vacancy, name='delete_saved_vacancy'),
    path('profile/saved-vacancies/', profile_resume_saved_vacancies, name='profile_resume_saved_vacancies'),
    path('resume/<int:pk>/delete/', views.delete_resume, name='delete_resume'),
    path('resume/<int:pk>/', views.resume_detail, name='resume_detail'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
