from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Task, TaskType, Student, Group


@admin.register(Student)
class StudentAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("group",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("group",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "group",
                    )
                },
            ),
        )
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("task_type", "priority", "deadline")


admin.site.register(TaskType)
admin.site.register(Group)
