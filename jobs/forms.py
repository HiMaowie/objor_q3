from django import forms
from .models import JobApplicant

class JobApplicantForm(forms.ModelForm):
    class Meta:
        model = JobApplicant
        fields = ['resume']
        widgets = {
            'resume': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }