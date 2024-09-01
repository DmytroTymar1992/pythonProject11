from django.db import models
from django.conf import settings  # Це використовується для посилання на модель User
from django.utils.text import slugify
from django.utils import timezone
from main.choices import EDUCATION_LEVEL_CHOICES
from ckeditor.fields import RichTextField


class Company(models.Model):
    EMPLOYEE_CHOICES = [
        (10, 'До 10 працівників '),
        (50, 'Від 10 до 50 працівників'),
        (100, 'Від 50 до 100 працівників'),
        (250, 'Від 100 до 250 працівників'),
        (500, 'Більше 500 працівників'),
    ]

    name = models.CharField(max_length=255, verbose_name="Назва")
    number_of_employees = models.IntegerField(choices=EMPLOYEE_CHOICES, verbose_name="Кількість працівників")
    logo = models.ImageField(upload_to='logos/', verbose_name="Логотип")
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'role': 'employer'}, on_delete=models.CASCADE, verbose_name="Адміністратор", related_name='administered_companies')
    description = models.TextField(null=True, blank=True, verbose_name="Опис")
    has_link = models.BooleanField(default=False, verbose_name="Посилання")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    def __str__(self):
        return self.name


class JobCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="Слаг")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class JobPositionGroup(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва")

    def __str__(self):
        return self.name


class JobPosition(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва")
    name_ru = models.CharField(max_length=255, verbose_name="Назва на російській мові")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="Слаг")
    categories = models.ManyToManyField(JobCategory, related_name="job_positions_by_category", verbose_name="Категорії")
    groups = models.ManyToManyField(JobPositionGroup, related_name="job_positions_by_group", verbose_name="Групи")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    image = models.ImageField(upload_to='articles/', verbose_name='Картинка')
    author = models.CharField(max_length=255, verbose_name='Автор')
    author_position = models.CharField(max_length=255, verbose_name='Посада автора')
    publication_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публікації')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Перегляди')

    def __str__(self):
        return self.title


class ArticleSection(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Текст')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='sections', verbose_name='Стаття')

    def __str__(self):
        return self.title


class CommentArticle(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments', verbose_name='Користувач')
    date_time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return self.text[:20]  # Повертає перші 20 символів коментаря


class Hashtag(models.Model):
    name = models.CharField(max_length=50, verbose_name="Хештег")

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    EMPLOYMENT_TYPE_CHOICES = [
        ('full', 'Повна зайнятісь'),
        ('part', 'Неповна зайнятісь'),
        ('shift', 'Позмінна робота'),
    ]

    WORK_TYPE_CHOICES = [
        ('internship', 'Стажування/практика'),
        ('remote', 'Відалена робота'),
        ('office', 'Робота в офісі'),
        ('hybrid', 'Гібридна робота'),
    ]

    STATUS_CHOICES = [
        ('standard', 'Стандарт'),
        ('standard_plus', 'Стандарт плюс'),
        ('hot', 'Гаряча'),
        ('hidden', 'Прихована'),
    ]

    EXPERIENCE_CHOICES = [
        ('no_experience', 'Можна без досвіду'),
        ('preferred_experience', 'Досвід буде перевагою'),
        ('one_year', 'Досвід від 1-го року'),
        ('two_years', 'Досвід від 2-х років'),
        ('more_than_five_years', 'Досвід більше 5 років'),
    ]

    SCHEDULE_CHOICES = [
        ('standard_5_2', 'Стандартний графік 5/2'),
        ('shift_4_4', 'Позмінний графік 4/4'),
        ('shift_2_2_4', 'Позмінний графік 2/2/4'),
        ('shift_4_2', 'Позмінний графік 4/2'),
        ('duty_1_3', 'Чергування доба/3 вихідних'),
        ('floating', 'Плаваючий графік'),
        ('free', 'Вільний графік'),
        ('part_time', 'Підробіток (не повний день)'),
    ]

    position = models.ForeignKey(JobPosition, on_delete=models.CASCADE, related_name='vacancies', verbose_name="Посада")
    position_comment = models.CharField(max_length=30, verbose_name="Коментар до посади", blank=True, null=True)
    city = models.ForeignKey('main.City', on_delete=models.CASCADE, verbose_name="Місто")
    address = models.CharField(max_length=255, verbose_name="Адреса", blank=True, null=True)
    phone_number = models.CharField(max_length=15, verbose_name="Номер телефону", blank=True, null=True)
    min_salary = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Зарплата мін", blank=True, null=True)
    max_salary = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Зарплата макс", blank=True, null=True)
    hashtags = models.ManyToManyField(Hashtag, verbose_name="Хештеги", blank=True)
    employment_type = models.CharField(max_length=10, choices=EMPLOYMENT_TYPE_CHOICES, verbose_name="Тип зайнятості",
                                       blank=True, null=True)
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL_CHOICES)
    description = models.TextField(verbose_name="Опис")
    social_networks = models.BooleanField(default=False, verbose_name="Соц.Мережі")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Компанія")
    publication_date = models.DateTimeField(default=timezone.now, verbose_name="Дата та час публікації")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, verbose_name="Статус")
    view_count = models.PositiveIntegerField(default=0, verbose_name="Кількість переглядів")
    experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, verbose_name="Досвід роботи",
                                  default='no_experience')
    schedule = models.CharField(max_length=20, choices=SCHEDULE_CHOICES, verbose_name="Графік роботи",
                                default='standard_5_2')

    def __str__(self):
        return f"{self.position} at {self.company}"


class VacancyLanguage(models.Model):
    BEGINNER = 'beginner'
    BASIC = 'basic'
    INTERMEDIATE = 'intermediate'
    ADVANCED = 'advanced'
    NATIVE = 'native'
    PROFICIENCY_LEVEL_CHOICES = [
        (BEGINNER, 'Початківець'),
        (BASIC, 'Базовий рівень'),
        (INTERMEDIATE, 'Впевнений користувач'),
        (ADVANCED, 'Вільно'),
        (NATIVE, 'Рідна'),
    ]

    language = models.ForeignKey('resume.Language', on_delete=models.CASCADE, related_name='vacancy_languages')
    proficiency_level = models.CharField(max_length=20, choices=PROFICIENCY_LEVEL_CHOICES)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='vacancy_languages')

    def __str__(self):
        return f'{self.language.name or ""} - {self.get_proficiency_level_display() or ""}'.strip()

    class Meta:
        verbose_name = 'Vacancy Language'
        verbose_name_plural = 'Vacancy Languages'
