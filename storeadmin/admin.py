from django.contrib import admin
from .models import StoreAdmin

@admin.register(StoreAdmin)
class StoreAdminAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_active', 'created_at')
    search_fields = ('username',)
    list_filter = ('is_active',)
