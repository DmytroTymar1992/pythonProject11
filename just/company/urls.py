from django.urls import path
from .views import create_vacancy, get_categories
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='company/main-employer-no-auth.html'), name='main-employer-no-auth'),
    path('vacancy/new/', create_vacancy, name='create_vacancy'),

    path('get_categories/', get_categories, name='get_categories'),

]
