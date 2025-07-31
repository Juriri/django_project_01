from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin  # Summernote 사용 시 필요

from todolist.models import Todo


@admin.register(Todo)
class TodoAdmin(SummernoteModelAdmin):  # SummernoteModelAdmin 상속
    list_display = ('title', 'description', 'is_completed', 'start_date', 'end_date')
    list_filter = ('is_completed',)
    search_fields = ('title',)
    ordering = ('start_date',)

    summernote_fields = ('description',)

    fieldsets = (
        ('Todo Info', {
            'fields': ('title', 'description', 'is_completed', 'completed_image')
        }),
        ('Date Range', {
            'fields': ('start_date', 'end_date')
        }),
    )
