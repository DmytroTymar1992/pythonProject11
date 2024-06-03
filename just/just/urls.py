from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from main.views import employer_login_view, seeker_login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='main/home.html'), name='home'),
    path('searcher/', include('searcher.urls')),
    path('company/', include('company.urls')),
    path('employer/login/', employer_login_view, name='employer_login'),
    path('seeker/login/', seeker_login_view, name='seeker_login'),
    path('employer/', include('employer.urls')),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
