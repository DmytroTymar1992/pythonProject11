from django import forms
from .models import Lead

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name', 'phone']

    name = forms.CharField(max_length=100, required=True, label="Ім'я")
    phone = forms.CharField(max_length=15, required=True, label="Номер телефону")