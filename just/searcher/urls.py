from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (register_seeker_step1,
                    register_seeker_step2,
                    register_seeker_step3,
                    registration_error,
                    create_resume,
                    edit_profile,
                    error_page
                    )
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('register/step1/', register_seeker_step1, name='register_seeker_step1'),
    path('register/step2/', register_seeker_step2, name='register_seeker_step2'),
    path('register/step3/', register_seeker_step3, name='register_seeker_step3'),
    path('registration-error/', views.registration_error, name='registration_error'),
    path('resume/create/', create_resume, name='create_resume'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/edit/error/', error_page, name='error_page'),
    path('profile/resumes/', views.profile_resume_list, name='profile_resume_list'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
