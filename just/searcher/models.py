from django.db import models
from django.conf import settings
from django.utils import timezone
from company.models import JobPosition
from django.core.exceptions import ValidationError


class Strength(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name or ""


class Resume(models.Model):
    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ]

    JOB_CHARACTER_CHOICES = [
        ('internship', 'Internship'),
        ('permanent', 'Permanent'),
        ('temporary', 'Temporary'),
    ]

    RELOCATE_YES = 'relocate_yes'
    RELOCATE_NO = 'relocate_no'
    RELOCATION_CHOICES = [
        (RELOCATE_YES, 'Можу виїхати за потреби'),
        (RELOCATE_NO, 'НЕ готовий до переїзду'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resumes')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    city = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(auto_now=True)

    desired_positions = models.ManyToManyField(JobPosition, related_name='resumes', blank=True)
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)
    employment_type = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_TYPE_CHOICES,
        default='full_time'
    )
    job_character = models.CharField(
        max_length=20,
        choices=JOB_CHARACTER_CHOICES,
        default='Internship'
    )
    relocation_ready = models.CharField(
        max_length=20,
        choices=RELOCATION_CHOICES,
        default=RELOCATE_NO
    )
    strengths = models.ManyToManyField('Strength', related_name='resumes', blank=True)

    def __str__(self):
        return f'{self.first_name or ""} {self.last_name or ""}'.strip()

    def clean(self):
        super().clean()
        if not self.desired_positions.exists():
            raise ValidationError({'desired_positions': 'Виберіть хоча б одну бажану позицію.'})

    class Meta:
        verbose_name = 'Resume'
        verbose_name_plural = 'Resumes'
        ordering = ['-date_created']


class Education(models.Model):
    EDUCATION_LEVEL_CHOICES = [
        ('high_school', 'Середня'),
        ('vocational_school', 'Середня спеціальна'),
        ('incomplete_higher', 'Незакінчена вища'),
        ('higher_education', 'Вища'),
    ]

    resume = models.ForeignKey('Resume', on_delete=models.CASCADE, related_name='educations')
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL_CHOICES)
    city = models.CharField(max_length=100)
    school = models.CharField(max_length=100)  # Назва школи з вільним введенням
    faculty = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_student = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.school or ""} ({self.get_education_level_display() or ""})'.strip()

    class Meta:
        verbose_name = 'Education'
        verbose_name_plural = 'Educations'
        ordering = ['start_date']


class WorkExperience(models.Model):
    resume = models.ForeignKey('Resume', on_delete=models.CASCADE, related_name='work_experiences')
    position = models.CharField(max_length=100, )
    company = models.CharField(max_length=100)  # Назва компанії з вільним введенням
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField()
    recommendation = models.FileField(upload_to='recommendations/', null=True, blank=True)

    def __str__(self):
        return f'{self.position or ""} at {self.company or ""}'.strip()

    class Meta:
        verbose_name = 'Work Experience'
        verbose_name_plural = 'Work Experiences'
        ordering = ['start_date']


class Course(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    resume = models.ForeignKey('Resume', on_delete=models.CASCADE, related_name='courses')
    certificate_link = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name or ""

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ['start_date']


class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name or ""


class UserLanguage(models.Model):
    BEGINNER = 'beginner'
    BASIC = 'basic'
    INTERMEDIATE = 'intermediate'
    ADVANCED = 'advanced'
    NATIVE = 'native'
    PROFICIENCY_LEVEL_CHOICES = [
        (BEGINNER, 'Початківець'),
        (BASIC, 'Базовий рівень'),
        (INTERMEDIATE, 'Впевнений користувач'),
        (ADVANCED, 'Вільно володію'),
        (NATIVE, 'Рідна'),
    ]

    language = models.ForeignKey('Language', on_delete=models.CASCADE, related_name='user_languages')
    proficiency_level = models.CharField(max_length=20, choices=PROFICIENCY_LEVEL_CHOICES)
    certificate_link = models.URLField(max_length=200, null=True, blank=True)
    resume = models.ForeignKey('Resume', on_delete=models.CASCADE, related_name='user_languages')

    def __str__(self):
        return f'{self.language.name or ""} - {self.get_proficiency_level_display() or ""}'.strip()

    class Meta:
        verbose_name = 'User Language'
        verbose_name_plural = 'User Languages'