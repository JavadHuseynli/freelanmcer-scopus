from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from projects.models import Project

User = get_user_model()

class Review(models.Model):
    """Müştərilərin freelancerlərə verdikləri rəy və qiymətlər"""
    
    # Əsas əlaqələr
    project = models.OneToOneField(
        Project,
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name='Layihə'
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews_given',
        verbose_name='Rəy verən (müştəri)'
    )
    freelancer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews_received',
        verbose_name='Rəy alınan (freelancer)'
    )
    
    # Qiymətləndirmə
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Qiymət (1-5)',
        help_text='1 - Çox pis, 5 - Əla'
    )
    
    # Müxtəlif sahələr üzrə qiymət
    quality_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Keyfiyyət',
        default=5
    )
    communication_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Ünsiyyət',
        default=5
    )
    timeliness_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Vaxtında təslim',
        default=5
    )
    
    # Yazılı rəy
    comment = models.TextField(
        verbose_name='Rəy',
        help_text='Freelancer haqqında təcrübənizi bölüşün'
    )
    
    # Təklif
    would_recommend = models.BooleanField(
        default=True,
        verbose_name='Tövsiyə edərəm'
    )
    would_hire_again = models.BooleanField(
        default=True,
        verbose_name='Yenidən işə tutaram'
    )
    
    # Tarix
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yaradılma tarixi'
    )
    
    class Meta:
        verbose_name = 'Rəy'
        verbose_name_plural = 'Rəylər'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.project.title} - {self.rating}★"
    
    @property
    def average_rating(self):
        """Bütün sahələrin ortalama qiyməti"""
        return round(
            (self.quality_rating + self.communication_rating + self.timeliness_rating) / 3, 
            1
        )