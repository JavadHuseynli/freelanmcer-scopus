
from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    """Layihə yaratma və yeniləmə forması"""
    
    class Meta:
        model = Project
        fields = [
            'title', 'description', 'category', 'budget_min', 'budget_max',
            'deadline', 'requirements', 'skills_required', 'urgency_level',
            'article_file'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Layihə başlığını daxil edin'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Layihənin təfərrüatlı təsvirini yazın'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'budget_min': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Minimum büdcə',
                'min': '0'
            }),
            'budget_max': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Maksimum büdcə',
                'min': '0'
            }),
            'deadline': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'requirements': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Əlavə tələblər və qeydlər'
            }),
            'skills_required': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Məsələn: EndNote, LaTeX, Academic Writing'
            }),
            'urgency_level': forms.Select(attrs={'class': 'form-select'}),
            'article_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            })
        }
    
    def clean(self):
        cleaned_data = super().clean()
        budget_min = cleaned_data.get('budget_min')
        budget_max = cleaned_data.get('budget_max')
        
        if budget_min and budget_max and budget_min > budget_max:
            raise forms.ValidationError('Minimum büdcə maksimum büdcədən böyük ola bilməz.')
        
        return cleaned_data