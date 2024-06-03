from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from main.models import User
from main.validators import CustomSeekerPasswordValidator
import re
from .models import Resume, Education, WorkExperience, Course, UserLanguage
from django.forms import inlineformset_factory
import datetime
from company.models import JobPosition
import logging
from django.contrib.auth import get_user_model
class PhoneVerificationForm(forms.Form):
    phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Номер телефону'})
    )

    def clean_phone(self):
        phone = self.cleaned_data['phone']
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
    city = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Місто'})
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
        fields = ('first_name', 'last_name', 'middle_name', 'city', 'birthday', 'password1', 'password2')

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


class ResumeForm(forms.ModelForm):
    desired_positions = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form__input create-resume__input-size-md',
            'id': 'id_desired_positions',
            'type': 'text',
            'placeholder': 'Виберіть посаду'
        })
    )

    employment_type = forms.MultipleChoiceField(
        choices=Resume.EMPLOYMENT_TYPE_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form__input-checkbox-item'
        })
    )

    job_character = forms.MultipleChoiceField(
        choices=Resume.JOB_CHARACTER_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form__input-checkbox-item'
        })
    )

    relocation_ready = forms.ChoiceField(
        choices=Resume.RELOCATION_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form__input-checkbox-item',
            'type': 'radio',
            'id': 'ready'
        })
    )



    class Meta:
        model = Resume
        fields = [
            'first_name', 'last_name', 'city', 'date_of_birth',
            'phone', 'email', 'avatar', 'desired_positions',
            'salary_min', 'salary_max', 'employment_type',
            'job_character', 'relocation_ready', 'strengths'
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form__input create-resume__input-size-lg'}),
            'last_name': forms.TextInput(attrs={'class': 'form__input create-resume__input-size-lg'}),
            'city': forms.TextInput(attrs={'class': 'form__input create-resume__input-size-lg'}),
            'date_of_birth': SelectDateWidget(),
            'phone': forms.TextInput(attrs={'class': 'form__input create-resume__input-size-lg'}),
            'email': forms.EmailInput(attrs={'class': 'form__input create-resume__input-size-lg', 'placeholder': 'example@gmail.com'}),

            'salary_min': forms.NumberInput(attrs={'class': 'form__input'}),
            'salary_max': forms.NumberInput(attrs={'class': 'form__input'}),


            'strengths': forms.SelectMultiple(attrs={'class': 'form__input create-resume__input-size-lg'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['city'].initial = user.city
            self.fields['phone'].initial = user.phone
            self.fields['date_of_birth'].initial = user.birthday
            self.fields['email'].initial = user.email
            self.fields['avatar'].initial = user.avatar



    def clean_desired_positions(self):
        desired_positions = self.cleaned_data.get('desired_positions')
        if desired_positions:
            # Розділяємо рядок на окремі позиції
            positions = [position.strip() for position in desired_positions.split(',')]
            job_positions = JobPosition.objects.filter(name__in=positions)
            return job_positions
        return desired_positions

    def save(self, commit=True):
        resume = super().save(commit=False)
        if commit:
            resume.save()
            self.save_m2m()
            desired_positions = self.cleaned_data.get('desired_positions')
            if desired_positions:
                resume.desired_positions.set(desired_positions)
        return resume

    def clean_employment_type(self):
        employment_type = self.cleaned_data['employment_type']
        if isinstance(employment_type, list):
            employment_type = employment_type[0]
        return employment_type

    def clean_job_character(self):
        job_character = self.cleaned_data['job_character']
        if isinstance(job_character, list):
            job_character = job_character[0]
        return job_character


class EducationForm(forms.ModelForm):
    start_month = forms.ChoiceField(
        choices=[('', 'Місяць')] + [(i, month) for i, month in enumerate([
            'Січень', 'Лютий', 'Березень', 'Квітень', 'Травень', 'Червень',
            'Липень', 'Серпень', 'Вересень', 'Жовтень', 'Листопад', 'Грудень'], 1)],
        required=False,
        widget=forms.Select(attrs={'class': 'form__input form__select create-resume__input-size-lg'})
    )
    start_year = forms.ChoiceField(
        choices=[('', 'Рік')] + [(year, year) for year in range(1950, datetime.datetime.now().year + 1)],
        required=False,
        widget=forms.Select(attrs={'class': 'form__input form__select create-resume__input-size-lg'})
    )
    end_month = forms.ChoiceField(
        choices=[('', 'Місяць')] + [(i, month) for i, month in enumerate([
            'Січень', 'Лютий', 'Березень', 'Квітень', 'Травень', 'Червень',
            'Липень', 'Серпень', 'Вересень', 'Жовтень', 'Листопад', 'Грудень'], 1)],
        required=False,
        widget=forms.Select(attrs={'class': 'form__input form__select create-resume__input-size-lg'})
    )
    end_year = forms.ChoiceField(
        choices=[('', 'Рік')] + [(year, year) for year in range(1950, datetime.datetime.now().year + 1)],
        required=False,
        widget=forms.Select(attrs={'class': 'form__input form__select create-resume__input-size-lg'})
    )

    class Meta:
        model = Education
        fields = ['education_level', 'city', 'school', 'faculty', 'start_date', 'end_date', 'is_student']
        widgets = {
            'education_level': forms.Select(
                attrs={'class': 'form__input form__select create-resume__input-size-lg', 'required': 'required'}),
            'city': forms.TextInput(
                attrs={'class': 'form__input create-resume__input-size-lg', 'required': 'required'}),
            'school': forms.TextInput(
                attrs={'class': 'form__input create-resume__input-size-lg', 'required': 'required'}),
            'faculty': forms.TextInput(
                attrs={'class': 'form__input create-resume__input-size-lg', 'required': 'required'}),
            'start_date': forms.HiddenInput(),
            'end_date': forms.HiddenInput(),
            'is_student': forms.CheckboxInput(attrs={'id': 'student'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_month = cleaned_data.get('start_month')
        start_year = cleaned_data.get('start_year')
        end_month = cleaned_data.get('end_month')
        end_year = cleaned_data.get('end_year')

        if start_month and start_year:
            cleaned_data['start_date'] = f'{start_year}-{int(start_month):02d}-01'
        else:
            cleaned_data['start_date'] = ''

        if end_month and end_year:
            cleaned_data['end_date'] = f'{end_year}-{int(end_month):02d}-01'
        else:
            cleaned_data['end_date'] = ''

        return cleaned_data


class WorkExperienceForm(forms.ModelForm):
    start_month = forms.ChoiceField(
        choices=[('', 'Місяць')] + [(i, month) for i, month in enumerate([
            'Січень', 'Лютий', 'Березень', 'Квітень', 'Травень', 'Червень',
            'Липень', 'Серпень', 'Вересень', 'Жовтень', 'Листопад', 'Грудень'], 1)],
        required=False,
        widget=forms.Select(attrs={'class': 'form__input form__select create-resume__input-size-lg'})
    )
    start_year = forms.ChoiceField(
        choices=[('', 'Рік')] + [(year, year) for year in range(1950, datetime.datetime.now().year + 1)],
        required=False,
        widget=forms.Select(attrs={'class': 'form__input form__select create-resume__input-size-lg'})
    )
    end_month = forms.ChoiceField(
        choices=[('', 'Місяць')] + [(i, month) for i, month in enumerate([
            'Січень', 'Лютий', 'Березень', 'Квітень', 'Травень', 'Червень',
            'Липень', 'Серпень', 'Вересень', 'Жовтень', 'Листопад', 'Грудень'], 1)],
        required=False,
        widget=forms.Select(attrs={'class': 'form__input form__select create-resume__input-size-lg'})
    )
    end_year = forms.ChoiceField(
        choices=[('', 'Рік')] + [(year, year) for year in range(1950, datetime.datetime.now().year + 1)],
        required=False,
        widget=forms.Select(attrs={'class': 'form__input form__select create-resume__input-size-lg'})
    )
    class Meta:
        model = WorkExperience
        fields = ['position', 'company', 'start_date', 'end_date', 'is_current', 'description', 'recommendation']
        widgets = {
            'position': forms.TextInput(
                attrs={'class': 'form__input create-resume__input-size-lg', 'required': 'required'}),
            'company': forms.TextInput(
                attrs={'class': 'form__input create-resume__input-size-lg', 'required': 'required'}),
            'start_date': forms.HiddenInput(),
            'end_date': forms.HiddenInput(),
            'is_current': forms.CheckboxInput(attrs={'id': 'work'}),
            'description': forms.Textarea(
                attrs={'class': 'create-resume__textarea create-resume__input-size-lg', 'required': 'required',
                       'placeholder': 'Розкажіть, що саме ви робили'}),
            'recommendation': forms.FileInput(attrs={'class': 'form__input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_month = cleaned_data.get('start_month')
        start_year = cleaned_data.get('start_year')
        end_month = cleaned_data.get('end_month')
        end_year = cleaned_data.get('end_year')

        if start_month and start_year:
            cleaned_data['start_date'] = datetime.date(int(start_year), int(start_month), 1)
        else:
            cleaned_data['start_date'] = None

        if end_month and end_year:
            cleaned_data['end_date'] = datetime.date(int(end_year), int(end_month), 1)
        else:
            cleaned_data['end_date'] = None

        return cleaned_data

class CourseForm(forms.ModelForm):
    start_month = forms.ChoiceField(
        choices=[('', 'Місяць')] + [(i, month) for i, month in enumerate([
            'Січень', 'Лютий', 'Березень', 'Квітень', 'Травень', 'Червень',
            'Липень', 'Серпень', 'Вересень', 'Жовтень', 'Листопад', 'Грудень'], 1)],
        required=False,
        widget=forms.Select(attrs={'class': 'form__input form__select create-resume__input-size-lg'})
    )
    start_year = forms.ChoiceField(
        choices=[('', 'Рік')] + [(year, year) for year in range(1950, datetime.datetime.now().year + 1)],
        required=False,
        widget=forms.Select(attrs={'class': 'form__input form__select create-resume__input-size-lg'})
    )
    end_month = forms.ChoiceField(
        choices=[('', 'Місяць')] + [(i, month) for i, month in enumerate([
            'Січень', 'Лютий', 'Березень', 'Квітень', 'Травень', 'Червень',
            'Липень', 'Серпень', 'Вересень', 'Жовтень', 'Листопад', 'Грудень'], 1)],
        required=False,
        widget=forms.Select(attrs={'class': 'form__input form__select create-resume__input-size-lg'})
    )
    end_year = forms.ChoiceField(
        choices=[('', 'Рік')] + [(year, year) for year in range(1950, datetime.datetime.now().year + 1)],
        required=False,
        widget=forms.Select(attrs={'class': 'form__input form__select create-resume__input-size-lg'})
    )


    class Meta:
        model = Course
        fields = ['name', 'start_date', 'end_date', 'certificate_link']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form__input create-resume__input-size-lg', 'required': 'required'}),
            'start_date': forms.DateInput(
                attrs={'class': 'form__input create-resume__input-size-lg', 'required': 'required', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form__input create-resume__input-size-lg', 'type': 'date'}),
            'certificate_link': forms.URLInput(attrs={'class': 'form__input create-resume__input-size-lg'}),
        }


    def clean(self):
        cleaned_data = super().clean()
        start_month = cleaned_data.get('start_month')
        start_year = cleaned_data.get('start_year')
        end_month = cleaned_data.get('end_month')
        end_year = cleaned_data.get('end_year')

        if start_month and start_year:
            cleaned_data['start_date'] = datetime.date(int(start_year), int(start_month), 1)
        else:
            cleaned_data['start_date'] = None

        if end_month and end_year:
            cleaned_data['end_date'] = datetime.date(int(end_year), int(end_month), 1)
        else:
            cleaned_data['end_date'] = None

        return cleaned_data

class UserLanguageForm(forms.ModelForm):
    class Meta:
        model = UserLanguage
        fields = ['language', 'proficiency_level', 'certificate_link']
        widgets = {
            'language': forms.Select(
                attrs={'class': 'form__input form__select create-resume__input-size-lg', 'required': 'required'}),
            'proficiency_level': forms.Select(
                attrs={'class': 'form__input form__select create-resume__input-size-lg', 'required': 'required'}),
            'certificate_link': forms.URLInput(attrs={'class': 'form__input create-resume__input-size-lg'}),
        }

EducationFormSet = inlineformset_factory(Resume, Education, form=EducationForm, extra=1, can_delete=True)
WorkExperienceFormSet = inlineformset_factory(Resume, WorkExperience, form=WorkExperienceForm, extra=1, can_delete=True)
CourseFormSet = inlineformset_factory(Resume, Course, form=CourseForm, extra=1, can_delete=True)
UserLanguageFormSet = inlineformset_factory(Resume, UserLanguage, form=UserLanguageForm, extra=1, can_delete=True)


User = get_user_model()
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'city', 'birthday', 'phone', 'email', 'avatar']
        widgets = {
            'birthday': SelectDateWidget(),
            'first_name': forms.TextInput(attrs={'class': 'form__input input-size-lg'}),
            'last_name': forms.TextInput(attrs={'class': 'form__input input-size-lg'}),
            'city': forms.TextInput(attrs={'class': 'form__input input-size-lg'}),
            'phone': forms.TextInput(attrs={'class': 'form__input input-size-lg'}),
            'email': forms.EmailInput(attrs={'class': 'form__input input-size-lg'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form__input input-size-lg'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if 'password' not in self.changed_data:
            user.password = User.objects.get(pk=user.pk).password
        if commit:
            user.save()
        return user