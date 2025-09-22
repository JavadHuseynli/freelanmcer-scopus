
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):      
    def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)
           for field in self.fields.values():
               field.widget.attrs['class'] = 'form-control'

    """Custom qeydiyyat forması"""
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user
    
class UserProfileForm(forms.ModelForm):
    """İstifadəçi profil yeniləmə forması"""
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'bio',
            'specialization', 'experience_years', 'hourly_rate'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'specialization': forms.TextInput(attrs={
                'placeholder': 'Məsələn: Elmi məqalə redaktəsi, Scopus dəstəyi'
            })
        }