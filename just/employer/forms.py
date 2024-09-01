from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
import base64
from main.models import User, City
from main.validators import EmployerPasswordValidator
from django.contrib.auth import get_user_model
from searcher.forms import SelectDateWidget

class EmailVerificationForm(forms.Form):
    email = forms.EmailField(
        max_length=255,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form__input', 'placeholder': 'Email'})
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Цей email вже зареєстрований.')
        return email

class EmailConfirmationCodeForm(forms.Form):
    code = forms.CharField(
        max_length=4,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Код підтвердження'})
    )

class EmployerRegistrationForm(UserCreationForm):
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
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'js_open form__input', 'placeholder': 'Місто'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form__input', 'placeholder': 'Пароль для входу'}
        ),
        help_text="Пароль має містити мінімум 8 символів.",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form__input', 'placeholder': 'Повторити пароль'}
        ),
        help_text="Пароль має містити мінімум 8 символів.",
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name', 'city_name', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Паролі не збігаються.")

        validator = EmployerPasswordValidator()
        validator.validate(password2)

        return password2

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        validator = EmployerPasswordValidator()
        validator.validate(password1)

        return password1

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'employer'  # Явно встановлюємо роль роботодавця
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user



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