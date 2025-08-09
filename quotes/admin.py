from django.contrib import admin
from .models import Quote

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'created_by', 'created_at')
    search_fields = ('text', 'author', 'created_by__username')
