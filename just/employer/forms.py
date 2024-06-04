from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from main.models import User
from main.validators import EmployerPasswordValidator
from django.contrib.auth import get_user_model
from searcher.forms import SelectDateWidget

class EmailVerificationForm(forms.Form):
    email = forms.EmailField(
        max_length=255,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form__input', 'placeholder': 'Email'})
    )

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
    city = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Місто'})
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
        fields = ('first_name', 'last_name', 'middle_name', 'city', 'password1', 'password2')

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