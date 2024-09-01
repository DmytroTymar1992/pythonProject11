from django.db import models
from django.conf import settings
from company.models import Vacancy





class SavedVacancy(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_vacancies')
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='saved_by_users')
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} saved {self.vacancy.position.name}"