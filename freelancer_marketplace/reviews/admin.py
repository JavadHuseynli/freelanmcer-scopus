
from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'project',
        'reviewer',
        'freelancer',
        'rating',
        'quality_rating',
        'communication_rating',
        'timeliness_rating',
        'created_at'
    )
    
    list_filter = (
        'rating',
        'would_recommend',
        'would_hire_again',
        'created_at'
    )
    
    search_fields = (
        'project__title',
        'reviewer__username',
        'freelancer__username',
        'comment'
    )
    
    readonly_fields = ('created_at', 'average_rating')
    
    fieldsets = (
        ('Əsas məlumatlar', {
            'fields': ('project', 'reviewer', 'freelancer')
        }),
        ('Qiymətləndirmə', {
            'fields': (
                'rating',
                'quality_rating',
                'communication_rating', 
                'timeliness_rating'
            )
        }),
        ('Rəy və tövsiyə', {
            'fields': ('comment', 'would_recommend', 'would_hire_again')
        }),
        ('Əlavə məlumatlar', {
            'fields': ('created_at', 'average_rating'),
            'classes': ('collapse',)
        })
    )
