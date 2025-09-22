
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class Project(models.Model):
    """Məqalə sifarişləri üçün Project modeli"""
    
    STATUS_CHOICES = [
        ('open', 'Açıq'),
        ('in_progress', 'İcrada'),
        ('completed', 'Tamamlandı'),
        ('cancelled', 'Ləğv edildi'),
    ]
    
    CATEGORY_CHOICES = [
        ('article_editing', 'Məqalə Redaktəsi'),
        ('scopus_support', 'Scopus Dəstəyi'),
        ('translation', 'Tərcümə'),
        ('research', 'Tədqiqat'),
        ('proofreading', 'Korrektor'),
        ('formatting', 'Formatlaşdırma'),
        ('other', 'Digər'),
    ]
    
    # Əsas məlumatlar
    title = models.CharField(
        max_length=200,
        verbose_name='Başlıq'
    )
    description = models.TextField(
        verbose_name='Təsvir'
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        verbose_name='Kateqoriya'
    )
    
    # İstifadəçi əlaqələri
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='my_projects',
        verbose_name='Müştəri'
    )
    assigned_freelancer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_projects',
        verbose_name='Təyin edilmiş freelancer'
    )
    
    # Büdcə və vaxt
    budget_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Minimum büdcə'
    )
    budget_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Maksimum büdcə'
    )
    deadline = models.DateTimeField(
        verbose_name='Son tarix'
    )
    
    # Status və fayllar
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='open',
        verbose_name='Status'
    )
    article_file = models.FileField(
        upload_to='articles/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='Məqalə faylı',
        help_text='PDF, DOC, DOCX formatlarında'
    )
    requirements = models.TextField(
        blank=True,
        null=True,
        verbose_name='Əlavə tələblər'
    )
    
    # Əlavə sahələr
    skills_required = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='Tələb olunan bacarıqlar',
        help_text='Vergül ilə ayrılmış'
    )
    urgency_level = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Aşağı'),
            ('medium', 'Orta'),
            ('high', 'Yüksək'),
            ('urgent', 'Təcili')
        ],
        default='medium',
        verbose_name='Təcillik səviyyəsi'
    )
    
    # Tarix sahələri
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yaradılma tarixi'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Yenilənmə tarixi'
    )
    
    class Meta:
        verbose_name = 'Layihə'
        verbose_name_plural = 'Layihələr'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def bid_count(self):
        """Bu layihəyə gələn təkliflərin sayı"""
        return self.bids.count()
    
    @property
    def average_bid(self):
        """Ortalama təklif qiyməti"""
        bids = self.bids.filter(status='active')
        if bids.exists():
            return bids.aggregate(avg=models.Avg('bid_amount'))['avg']
        return None
    
    @property
    def is_open(self):
        return self.status == 'open'
    
    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'pk': self.pk})
