from django import forms
from django.contrib.auth.forms import AuthenticationForm
import re
from django.contrib.auth.forms import UserChangeForm
from .models import User


class EmployerLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={'autofocus': True})
    )

class SeekerLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Phone",
        max_length=15,
        widget=forms.TextInput(attrs={'autofocus': True})
    )

    def clean_username(self):
        phone = self.cleaned_data['username']
        phone = re.sub(r'\D', '', phone)  # Видалити всі нецифрові символи

        # Перевірити та нормалізувати номер
        if phone.startswith('380') and len(phone) == 12:
            phone = phone[2:]  # Видалити '380'
        elif phone.startswith('80') and len(phone) == 11:
            phone = phone[1:]  # Видалити '8'
        elif phone.startswith('0') and len(phone) == 10:
            pass  # Нічого не робити, номер вже нормальний
        elif len(phone) == 9:
            phone = '0' + phone  # Додати '0' на початок
        else:
            raise forms.ValidationError('Неправильний формат номера телефону.')

        return phone


class CustomUserChangeForm(UserChangeForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = '__all__'

    def clean_password(self):
        # Повертаємо початкове значення пароля, якщо воно не задано у формі
        return self.initial.get('password')