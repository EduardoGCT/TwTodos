from django.contrib import admin

from .models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ("title", "priority", "deadline", "finished_at", "created_at")
    list_filter = ("priority", "finished_at")
    search_fields = ("title", "description")
    ordering = ("priority", "deadline")
