from django import forms
from .models import Vacancy, JobPosition
from main.models import City

class VacancyForm(forms.ModelForm):
    position = forms.CharField(widget=forms.TextInput(attrs={'id': 'id_position', 'class': 'form__input create-vacancy__input-size js_open universal-form'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'id': 'id_city', 'class': 'form__input create-vacancy__input-size js_open universal-form'}))
    class Meta:
        model = Vacancy
        fields = ['position', 'position_comment', 'city', 'address', 'phone_number', 'min_salary',
                  'max_salary', 'hashtags', 'employment_type', 'education_level', 'description',
                  'social_networks', 'status', 'experience', 'schedule']
        widgets = {
            'position_comment': forms.TextInput(attrs={'class': 'form__input create-vacancy__input-size',
                                                       'id': 'id_position_comment',
                                                       'placeholder': 'Нічні зміни'}),

            'address': forms.TextInput(attrs={'class': 'form__input create-vacancy__input-size'}),
            'phone_number': forms.TextInput(attrs={'class': 'form__input create-vacancy__input-size',
                                                   'id': 'id_phone_number',
                                                   'placeholder': '+380-00-00-00-000',
                                                   'type': 'tel'}),
            'min_salary': forms.NumberInput(attrs={'class': 'form__input salary__input'}),
            'max_salary': forms.NumberInput(attrs={'class': 'form__input salary__input'}),
            'hashtags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'employment_type': forms.Select(attrs={'class': 'form-control'}),

            'description': forms.Textarea(attrs={'class': 'create-vacancy__textarea'}),
            'social_networks': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'schedule': forms.Select(attrs={'class': 'select__input'}),
        }

    def clean_position(self):
        position_name = self.cleaned_data['position']
        position = JobPosition.objects.filter(name=position_name).first()
        return position

    def clean_city(self):
        city_name = self.cleaned_data['city']
        city = City.objects.filter(name=city_name).first()
        return city  # Повертаємо об'єкт City
