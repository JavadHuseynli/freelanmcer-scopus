
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Custom User modeli - Freelancer və Müştəri rolları ilə"""
    
    ROLE_CHOICES = [
        ('freelancer', 'Freelancer'),
        ('customer', 'Müştəri'),
    ]
    scopus_author_id = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        verbose_name='Scopus Author ID',
        help_text='Məsələn: 123456789'
    )
    h_index = models.PositiveIntegerField(
        default=0,
        verbose_name='H-index',
        help_text='Google Scholar və ya Scopus H-index'
    )
    scopus_h_index = models.PositiveIntegerField(
        default=0,
        verbose_name='Scopus H-index'
    )
    total_citations = models.PositiveIntegerField(
        default=0,
        verbose_name='Ümumi istinadlar sayı'
    )
    total_publications = models.PositiveIntegerField(
        default=0,
        verbose_name='Nəşr sayı'
    )
    orcid_id = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name='ORCID ID',
        help_text='Məsələn: 0000-0000-0000-0000'
    )
    google_scholar_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='Google Scholar profili'
    )
    research_interests = models.TextField(
        blank=True,
        null=True,
        verbose_name='Tədqiqat sahələri',
        help_text='Vergüllərlə ayırın'
    )
    
    # Academic credentials
    academic_degree = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Akademik dərəcə',
        help_text='PhD, Prof., Dr. və s.'
    )
    university_affiliation = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Universitet əlaqəsi'
    )

    # Əsas sahələr
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='customer',
        verbose_name='Rol'
    )
    phone = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        verbose_name='Telefon'
    )
    bio = models.TextField(
        blank=True, 
        null=True,
        verbose_name='Haqqında'
    )
    
    # Freelancer üçün əlavə sahələr
    specialization = models.CharField(
        max_length=200, 
        blank=True, 
        null=True,
        help_text="Məsələn: Elmi məqalə redaktəsi, Scopus indeksləşdirmə",
        verbose_name='İxtisaslaşma'
    )
    experience_years = models.PositiveIntegerField(
        default=0,
        verbose_name='Təcrübə (il)'
    )
    hourly_rate = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True,
        verbose_name='Saatlıq tarif'
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name='Təsdiqlənib'
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
        verbose_name = 'İstifadəçi'
        verbose_name_plural = 'İstifadəçilər'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def is_freelancer(self):
        return self.role == 'freelancer'
    
    @property
    def is_customer(self):
        return self.role == 'customer'