
from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'project',
        'payer',
        'receiver',
        'amount',
        'payment_type',
        'status',
        'created_at'
    )
    
    list_filter = ('status', 'payment_type', 'created_at')
    search_fields = (
        'project__title',
        'payer__username',
        'receiver__username',
        'transaction_id'
    )
    
    readonly_fields = ('created_at',)