
from django.db import models
from django.contrib.auth import get_user_model
from projects.models import Project

User = get_user_model()

class Bid(models.Model):
    """Freelancerlərin layihələrə təklifləri"""
    
    STATUS_CHOICES = [
        ('active', 'Aktiv'),
        ('accepted', 'Qəbul edildi'),
        ('rejected', 'Rədd edildi'),
        ('withdrawn', 'Geri çəkildi'),
    ]
    
    # Əsas əlaqələr
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='bids',
        verbose_name='Layihə'
    )
    freelancer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='my_bids',
        verbose_name='Freelancer'
    )
    
    # Təklif məlumatları
    bid_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Təklif məbləği'
    )
    delivery_time = models.PositiveIntegerField(
        verbose_name='Təhvil müddəti (gün)',
        help_text='Neçə gün ərzində işi bitirəcəksiniz'
    )
    proposal = models.TextField(
        verbose_name='Təklif təsviri',
        help_text='Nəyə görə bu işi sizə verməlidirlər?'
    )
    
    # Status və tarixlər
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='Status'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yaradılma tarixi'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Yenilənmə tarixi'
    )
    
    class Meta:
        verbose_name = 'Təklif'
        verbose_name_plural = 'Təkliflər'
        ordering = ['-created_at']
        # Bir freelancer bir layihəyə yalnız bir təklif verə bilər
        unique_together = ['project', 'freelancer']
    
    def __str__(self):
        return f"{self.freelancer.username} - {self.project.title} ({self.bid_amount}₼)"
    
    @property
    def is_active(self):
        return self.status == 'active'
    
    @property
    def is_accepted(self):
        return self.status == 'accepted'