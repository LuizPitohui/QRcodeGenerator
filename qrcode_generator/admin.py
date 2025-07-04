from django.contrib import admin
from .models import QRCodeHistory


@admin.register(QRCodeHistory)
class QRCodeHistoryAdmin(admin.ModelAdmin):
    """
    Configuração do Django Admin para QRCodeHistory
    """
    list_display = ['content_preview', 'qr_type', 'created_at', 'ip_address']
    list_filter = ['qr_type', 'created_at']
    search_fields = ['content', 'ip_address']
    readonly_fields = ['created_at', 'ip_address', 'user_agent']
    ordering = ['-created_at']
    list_per_page = 25
    
    def content_preview(self, obj):
        """Exibe prévia do conteúdo"""
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Conteúdo'
    
    def has_add_permission(self, request):
        """Remove permissão de adicionar via admin"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Remove permissão de editar via admin"""
        return False

