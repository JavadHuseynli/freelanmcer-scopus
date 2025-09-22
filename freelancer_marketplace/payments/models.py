
from django.db import models
from django.contrib.auth import get_user_model
from projects.models import Project

User = get_user_model()

class Payment(models.Model):
    """Ödəniş izləmə sistemi"""
    
    STATUS_CHOICES = [
        ('pending', 'Gözləmədə'),
        ('paid', 'Ödənildi'),
        ('failed', 'Uğursuz'),
        ('refunded', 'Geri qaytarıldı'),
    ]
    
    TYPE_CHOICES = [
        ('project_payment', 'Layihə ödənişi'),
        ('milestone_payment', 'Mərhələ ödənişi'),
        ('bonus', 'Bonus'),
        ('refund', 'Geri qaytarma'),
    ]
    
    # Əsas məlumatlar
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Layihə'
    )
    payer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments_made',
        verbose_name='Ödəyici (müştəri)'
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments_received',
        verbose_name='Alan (freelancer)'
    )
    
    # Ödəniş məlumatları
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Məbləğ'
    )
    payment_type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        default='project_payment',
        verbose_name='Ödəniş növü'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Status'
    )
    
    # Əlavə məlumatlar
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Açıqlama'
    )
    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Tranzaksiya ID'
    )
    
    # Tarixlər
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yaradılma tarixi'
    )
    paid_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Ödəniş tarixi'
    )
    
    class Meta:
        verbose_name = 'Ödəniş'
        verbose_name_plural = 'Ödənişlər'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.project.title} - {self.amount}₼ ({self.get_status_display()})"
