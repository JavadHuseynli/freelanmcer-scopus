
from django import forms
from .models import Bid

class BidForm(forms.ModelForm):
    """Bid yaratma forması"""
    
    class Meta:
        model = Bid
        fields = ['bid_amount', 'delivery_time', 'proposal']
        widgets = {
            'bid_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Təklif məbləği',
                'min': '1'
            }),
            'delivery_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Neçə gün',
                'min': '1'
            }),
            'proposal': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Nəyə görə bu işi sizə verməlidirlər? Təcrübənizi və yanaşmanızı təsvir edin...'
            })
        }
        labels = {
            'bid_amount': 'Təklif məbləği (₼)',
            'delivery_time': 'Təhvil müddəti (gün)',
            'proposal': 'Təklif təsviri'
        }
    
    def clean_bid_amount(self):
        bid_amount = self.cleaned_data.get('bid_amount')
        if bid_amount and bid_amount <= 0:
            raise forms.ValidationError('Təklif məbləği sıfırdan böyük olmalıdır.')
        return bid_amount
    
    def clean_delivery_time(self):
        delivery_time = self.cleaned_data.get('delivery_time')
        if delivery_time and delivery_time <= 0:
            raise forms.ValidationError('Təhvil müddəti ən azı 1 gün olmalıdır.')
        if delivery_time and delivery_time > 365:
            raise forms.ValidationError('Təhvil müddəti 365 gündən çox ola bilməz.')
        return delivery_time