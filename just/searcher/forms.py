from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from main.models import User, City
from main.validators import CustomSeekerPasswordValidator
import re
from django.core.files.base import ContentFile
import base64

import datetime

import logging
from django.contrib.auth import get_user_model
from django.contrib import messages
from main.utils import clean_phone


class PhoneVerificationForm(forms.Form):
    phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Номер телефону'})
    )

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        return clean_phone(phone)

class ConfirmationCodeForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Код підтвердження'})
    )

class SeekerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Ім’я'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Прізвище'})
    )
    middle_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'По батькові'})
    )
    city_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'js_open form__input', 'placeholder': 'Місто'})
    )


    birthday = forms.DateField(
        required=False,
        widget=forms.SelectDateWidget(
            years=range(1900, 2024),
            attrs={'class': 'form__input'}
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form__input', 'placeholder': 'Пароль для входу'}
        ),
        help_text="Пароль має містити рівно 4 цифри.",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form__input', 'placeholder': 'Повторити пароль'}
        ),
        help_text="Пароль має містити рівно 4 цифри.",
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name', 'city_name', 'birthday', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        city_name = cleaned_data.get('city_name')
        if city_name:
            try:
                city = City.objects.get(name__iexact=city_name)
                cleaned_data['city'] = city
            except City.DoesNotExist:
                self.add_error('city_name', 'Invalid city name.')
        return cleaned_data


    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Паролі не збігаються.")

        validator = CustomSeekerPasswordValidator()
        validator.validate(password2)

        return password2

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        validator = CustomSeekerPasswordValidator()
        validator.validate(password1)

        return password1

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'seeker'  # Явно встановлюємо роль пошуковця
        # Зберігаємо номер телефону із сесії
        if 'phone' in self.initial:
            user.phone = self.initial['phone']
        if commit:
            user.save()
        return user

class SelectDateWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        years = [('', 'Рік')] + [(year, year) for year in range(1950, datetime.datetime.now().year - 14)]
        months = [('', 'Місяць')] + [
            (1, 'Січень'), (2, 'Лютий'), (3, 'Березень'), (4, 'Квітень'),
            (5, 'Травень'), (6, 'Червень'), (7, 'Липень'), (8, 'Серпень'),
            (9, 'Вересень'), (10, 'Жовтень'), (11, 'Листопад'), (12, 'Грудень')
        ]
        days = [('', 'День')] + [(day, day) for day in range(1, 32)]

        widgets = [
            forms.Select(attrs={'class': 'form__input form__select create-resume__input-size-lg'}, choices=days),
            forms.Select(attrs={'class': 'form__input form__select create-resume__input-size-lg'}, choices=months),
            forms.Select(attrs={'class': 'form__input form__select create-resume__input-size-lg'}, choices=years),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            if isinstance(value, str):
                try:
                    value = datetime.datetime.strptime(value, '%Y-%m-%d')
                except ValueError:
                    return [None, None, None]
            return [value.day, value.month, value.year]
        return [None, None, None]

    def compress(self, values):
        if values:
            try:
                day, month, year = values
                if day and month and year:
                    return f"{year}-{month:02d}-{day:02d}"
            except ValueError:
                pass
        return None

    def value_from_datadict(self, data, files, name):
        day = data.get(f'{name}_0')
        month = data.get(f'{name}_1')
        year = data.get(f'{name}_2')
        if day and month and year:
            return f'{year}-{month}-{day}'
        return None


User = get_user_model()
class UserProfileForm(forms.ModelForm):
    city_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'js_open form__input input-size-lg', 'placeholder': 'Місто'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'city_name', 'birthday', 'phone', 'email', 'avatar']
        widgets = {
            'birthday': SelectDateWidget(),
            'first_name': forms.TextInput(attrs={'class': 'form__input input-size-lg'}),
            'last_name': forms.TextInput(attrs={'class': 'form__input input-size-lg'}),
            'phone': forms.TextInput(attrs={'class': 'form__input input-size-lg'}),
            'email': forms.EmailInput(attrs={'class': 'form__input input-size-lg'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form__input input-size-lg'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.city:
            self.fields['city_name'].initial = self.instance.city.name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        return clean_phone(phone)

    def clean(self):
        cleaned_data = super().clean()
        city_name = cleaned_data.get('city_name')
        if city_name:
            try:
                city = City.objects.get(name__iexact=city_name)
                cleaned_data['city'] = city
            except City.DoesNotExist:
                self.add_error('city_name', 'Invalid city name.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        cropped_avatar = self.data.get('cropped_avatar')
        if cropped_avatar:
            format, imgstr = cropped_avatar.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'avatar.{ext}')
            user.avatar = data
        if commit:
            user.save()
        return user


class VacancySearchForm(forms.Form):
    title = forms.CharField(max_length=100, required=False, label='Назва вакансії', widget=forms.TextInput(attrs={
        'id': 'id_position', 'class': 'search-location__input js_open', 'placeholder': 'Менеджер'
    }))
    city = forms.CharField(max_length=100, required=False, label='Місто', widget=forms.TextInput(attrs={
        'id': 'id_city', 'class': 'search-location__select js_open', 'placeholder': 'Вся Україна'
    }))