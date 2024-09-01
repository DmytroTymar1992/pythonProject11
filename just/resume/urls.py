from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import create_resume

urlpatterns = [
    path('', create_resume, name='create_resume'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)