from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from company.models import Company

class UserManager(BaseUserManager):
    def create_user(self, email=None, phone=None, password=None, **extra_fields):
        if not email and not phone:
            raise ValueError('The Email or Phone field must be set')
        if email:
            email = self.normalize_email(email)
            user = self.model(email=email, **extra_fields)
        else:
            user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.clean()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email=email, password=password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('seeker', 'Пошуковець'),
        ('employer', 'Роботодавець'),
    ]

    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    middle_name = models.CharField(max_length=30, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.SET_NULL, related_name='users')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set', blank=True)

    USERNAME_FIELD = 'email'  # This will be dynamically checked during authentication
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email if self.email else self.phone

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    @property
    def username_field(self):
        return 'email' if self.role == 'employer' else 'phone'

    def clean(self):
        super().clean()
        if self.pk is None:  # Перевірка тільки під час створення нового користувача
            if self.role == 'seeker':
                if not self.phone:
                    raise ValidationError('Phone number must be provided for seekers.')
                if not self.password or len(self.password) != 4 or not self.password.isdigit():
                    raise ValidationError('Password must be exactly 4 digits for seekers.')
            elif self.role == 'employer':
                if not self.email:
                    raise ValidationError('Email must be provided for employers.')
                if self.company is None:
                    raise ValidationError('Company must be provided for employers.')
                if not self.password or len(self.password) < 8 or self.password.isdigit():
                    raise ValidationError('Password must be at least 8 characters and not entirely numeric for employers.')
