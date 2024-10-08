# Generated by Django 4.2.13 on 2024-08-29 21:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0004_alter_vacancy_description'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('resume', '0002_resume_positions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name="Ім'я")),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('new', 'Новий'), ('in_progress', 'В роботі'), ('rejected', 'Відхилено'), ('interview', 'Співбесіда'), ('reserve', 'Резерв')], default='new', max_length=20, verbose_name='Статус')),
                ('viewed', models.BooleanField(default=False, verbose_name='Переглянуто')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата та час відгуку')),
                ('job_seeker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_feedbacks', to=settings.AUTH_USER_MODEL)),
                ('lead', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='feedback.lead', verbose_name='Лід')),
                ('resume', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='feedbacks', to='resume.resume', verbose_name='Резюме')),
                ('vacancy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.vacancy', verbose_name='Вакансія')),
            ],
        ),
    ]
