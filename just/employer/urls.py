from django.urls import path
from .views import register_employer_step1, register_employer_step2, register_employer_step3, registration_error, edit_profile, profile_vacancy_list
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('register/step1/', register_employer_step1, name='register_employer_step1'),
    path('register/step2/', register_employer_step2, name='register_employer_step2'),
    path('register/step3/', register_employer_step3, name='register_employer_step3'),
    path('register/error/', registration_error, name='registration_error'),
    path('profile/edit/', edit_profile, name='employer_profile'),
    path('profile/vacancy/', profile_vacancy_list, name='profile_vacancy_list'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)