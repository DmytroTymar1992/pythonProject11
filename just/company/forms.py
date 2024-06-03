from django import forms
from .models import Vacancy, JobPosition

class VacancyForm(forms.ModelForm):
    position_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form__input create-vacancy__input-size',
            'id': 'id_position_name',
            'type': 'text',
            'placeholder': 'Менеджер з продажу'
        })
    )

    class Meta:
        model = Vacancy
        fields = [
            'position_name', 'position_comment', 'city', 'address', 'phone_number',
            'min_salary', 'max_salary', 'hashtags', 'employment_type',
            'work_type', 'description', 'social_networks', 'company', 'status'
        ]
        widgets = {
            'position_comment': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'min_salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'hashtags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'employment_type': forms.Select(attrs={'class': 'form-control'}),
            'work_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'social_networks': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'company': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        position_name = cleaned_data.get('position_name')
        if position_name:
            try:
                position = JobPosition.objects.get(name=position_name)
                cleaned_data['position'] = position
            except JobPosition.DoesNotExist:
                self.add_error('position_name', 'Посада не знайдена.')
        return cleaned_data

    def save(self, commit=True):
        vacancy = super().save(commit=False)
        position_name = self.cleaned_data.get('position_name')
        if position_name:
            vacancy.position = JobPosition.objects.get(name=position_name)
        if commit:
            vacancy.save()
            self.save_m2m()
        return vacancy
