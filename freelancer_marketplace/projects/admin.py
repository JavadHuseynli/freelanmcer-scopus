
from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Project modelinin admin panel konfiqurasiyası"""
    
    list_display = (
        'title', 
        'customer', 
        'category', 
        'status', 
        'budget_min',
        'budget_max',
        'deadline',
        'bid_count',
        'created_at'
    )
    
    list_filter = (
        'status', 
        'category', 
        'urgency_level',
        'created_at',
        'deadline'
    )
    
    search_fields = (
        'title', 
        'description', 
        'customer__username',
        'customer__email'
    )
    
    readonly_fields = ('created_at', 'updated_at', 'bid_count')
    
    fieldsets = (
        ('Əsas məlumatlar', {
            'fields': ('title', 'description', 'category', 'customer')
        }),
        ('Büdcə və vaxt', {
            'fields': ('budget_min', 'budget_max', 'deadline', 'urgency_level')
        }),
        ('Status və təyinat', {
            'fields': ('status', 'assigned_freelancer')
        }),
        ('Fayllar və tələblər', {
            'fields': ('article_file', 'requirements', 'skills_required'),
            'classes': ('collapse',)
        }),
        ('Əlavə məlumatlar', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def bid_count(self, obj):
        return obj.bid_count
    bid_count.short_description = 'Təkliflər sayı'