from django.contrib import admin
from .models import ToDoItem


# Register your models here.
@admin.register(ToDoItem)
class ToDoItemAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_completed", "created_at", "updated_at")
    list_filter = [
        "is_completed",
    ]
    search_fields = [
        "title",
    ]
