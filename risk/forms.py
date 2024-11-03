from django import forms
from django.contrib.auth.models import User
from .models import Company, Prj, Risk
# , UserCompany

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'  # Include all fields from the Company model
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Prj
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'user': forms.HiddenInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control'}),
            'estimated_finish_date': forms.DateInput(attrs={'class': 'form-control'}),
            'client': forms.TextInput(attrs={'class': 'form-control'}),
            'technology_stack': forms.Textarea(attrs={'class': 'form-control'}),
            'size_bucket': forms.Select(attrs={'class': 'form-control'}),
            'total_budget': forms.NumberInput(attrs={'class': 'form-control'}),
            'team_size': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('name'):
            self.add_error('name', 'Project name is required.')
        return cleaned_data

class RiskForm(forms.ModelForm):
    class Meta:
        model = Risk
        fields = '__all__'
        widgets = {
            'project': forms.HiddenInput(attrs={'class': 'form-control'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


