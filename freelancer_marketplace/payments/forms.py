
from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    """Ödəniş yaratma forması"""
    
    class Meta:
        model = Payment
        fields = ['amount', 'payment_type', 'description']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ödəniş məbləği',
                'min': '1'
            }),
            'payment_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ödəniş açıqlaması (məsələn: Layihənin tamamlanması üçün)'
            })
        }
        labels = {
            'amount': 'Məbləğ (₼)',
            'payment_type': 'Ödəniş növü',
            'description': 'Açıqlama'
        }
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount and amount <= 0:
            raise forms.ValidationError('Ödəniş məbləği sıfırdan böyük olmalıdır.')
        if amount and amount > 50000:
            raise forms.ValidationError('Ödəniş məbləği 50,000₼-dən çox ola bilməz.')
        return amount
