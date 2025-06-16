"""
Настройка админ-панели для модели MenuItem.
"""
from django.contrib import admin
from .models import MenuItem


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    """
    Админ-панель для управления пунктами меню.
    """
    list_display = ('title', 'menu_name', 'url', 'parent', 'order')
    list_filter = ('menu_name',)
    search_fields = ('title', 'url', 'menu_name')
    list_editable = ('order',)
    list_per_page = 25
    ordering = ('menu_name', 'order', 'title')

    fieldsets = (
        (None, {
            'fields': ('title', 'url', 'menu_name', 'order')
        }),
        ('Иерархия', {
            'fields': ('parent',),
        }),
    )

    def get_queryset(self, request):
        """
        Оптимизация запросов для отображения связанных объектов.
        """
        return super().get_queryset(request).select_related('parent')
