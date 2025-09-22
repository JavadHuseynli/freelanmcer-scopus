
from django.contrib import admin
from .models import Bid

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = (
        'project',
        'freelancer', 
        'bid_amount',
        'delivery_time',
        'status',
        'created_at'
    )
    
    list_filter = ('status', 'created_at')
    search_fields = (
        'project__title',
        'freelancer__username',
        'proposal'
    )
    
    readonly_fields = ('created_at', 'updated_at')