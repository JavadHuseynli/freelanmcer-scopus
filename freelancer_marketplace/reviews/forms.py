
from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    """Rəy yazmaq forması"""
    
    class Meta:
        model = Review
        fields = [
            'rating', 'quality_rating', 'communication_rating', 'timeliness_rating',
            'comment', 'would_recommend', 'would_hire_again'
        ]
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}, choices=[(i, f'{i} ulduz') for i in range(1, 6)]),
            'quality_rating': forms.Select(attrs={'class': 'form-select'}, choices=[(i, f'{i} ulduz') for i in range(1, 6)]),
            'communication_rating': forms.Select(attrs={'class': 'form-select'}, choices=[(i, f'{i} ulduz') for i in range(1, 6)]),
            'timeliness_rating': forms.Select(attrs={'class': 'form-select'}, choices=[(i, f'{i} ulduz') for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Freelancer ilə təcrübənizi və işin keyfiyyətini təsvir edin...'
            }),
            'would_recommend': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'would_hire_again': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        labels = {
            'rating': 'Ümumi qiymət',
            'quality_rating': 'İş keyfiyyəti',
            'communication_rating': 'Ünsiyyət',
            'timeliness_rating': 'Vaxtında təslim',
            'comment': 'Rəy',
            'would_recommend': 'Bu freelancer-i başqalarına tövsiyə edirəm',
            'would_hire_again': 'Yenidən işə tutaram'
        }
