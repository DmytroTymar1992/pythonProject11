from django.urls import path
from .views import employer_login_view, seeker_login_view

urlpatterns = [
    # ваші інші маршрути
    path('employer/login/', employer_login_view, name='employer_login'),
    path('seeker/login/', seeker_login_view, name='seeker_login'),
]