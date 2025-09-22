
from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """User modelinin admin paneli"""
    
    # Siyahıda göstəriləcək sütunlar
    list_display = (
        'username',
        'email', 
        'role',
        'specialization',
        'is_verified',
        'is_active',
        'created_at'
    )
    
    # Sağ tərəfdə filtrlər
    list_filter = (
        'role',
        'is_verified', 
        'is_active',
        'created_at'
    )
    
    # Axtarış sahələri
    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
        'specialization'
    )
    
    # Redaktə səhifəsində sahələrin qruplaşması
    fieldsets = (
        ('Əsas məlumatlar', {
            'fields': ('username', 'email', 'first_name', 'last_name')
        }),
        ('Parol', {
            'fields': ('password',),
            'classes': ('collapse',)
        }),
        ('Rol və statuslar', {
            'fields': ('role', 'is_verified', 'is_active', 'is_staff', 'is_superuser')
        }),
        ('Freelancer məlumatları', {
            'fields': ('specialization', 'experience_years', 'hourly_rate', 'phone', 'bio'),
            'description': 'Bu sahələr əsasən freelancerlər üçündür'
        }),
    )
    
    # Yalnız oxunan sahələr
    readonly_fields = ('created_at', 'updated_at')
    
    # Sıralama
    ordering = ['-created_at']
