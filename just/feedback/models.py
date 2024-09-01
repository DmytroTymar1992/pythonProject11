from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.conf import settings


class Lead(models.Model):
    name = models.CharField(max_length=255, verbose_name="Ім'я")
    phone = models.CharField(max_length=20, verbose_name="Телефон")

    def __str__(self):
        return f"{self.name} - {self.phone}"


class Feedback(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новий'),
        ('in_progress', 'В роботі'),
        ('rejected', 'Відхилено'),
        ('interview', 'Співбесіда'),
        ('reserve', 'Резерв'),
    ]

    vacancy = models.ForeignKey('company.Vacancy', on_delete=models.CASCADE, verbose_name="Вакансія")
    job_seeker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_feedbacks', null=True, blank=True,)
    lead = models.ForeignKey(Lead, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Лід")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    viewed = models.BooleanField(default=False, verbose_name="Переглянуто")
    resume = models.ForeignKey('resume.Resume', null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Резюме", related_name='feedbacks',)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата та час відгуку")