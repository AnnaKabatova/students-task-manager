from django.urls import path

from manager.views import (
    index,
    GroupListView,
    GroupCreateView,
    GroupDeleteView,
    GroupUpdateView,
    TaskTypeListView,
    TaskTypeCreateView,
    TaskTypeUpdateView,
    TaskTypeDeleteView,
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    update_completion,
    TaskDeleteView,
    StudentListView,
    StudentDetailView,
    StudentCreateView,
    StudentGroupUpdateView,
    StudentDeleteView,
)

urlpatterns = [
    path("", index, name="index"),
    path(
        "groups/",
        GroupListView.as_view(),
        name="group-list",
    ),
    path(
        "groups/create/",
        GroupCreateView.as_view(),
        name="group-create",
    ),
    path(
        "groups/<int:pk>/update/",
        GroupUpdateView.as_view(),
        name="group-update",
    ),
    path(
        "groups/<int:pk>/delete/",
        GroupDeleteView.as_view(),
        name="group-delete",
    ),
    path(
        "task_types/",
        TaskTypeListView.as_view(),
        name="task-type-list",
    ),
    path(
        "task_types/create/",
        TaskTypeCreateView.as_view(),
        name="task-type-create",
    ),
    path(
        "task_types/<int:pk>/update/",
        TaskTypeUpdateView.as_view(),
        name="task-type-update",
    ),
    path(
        "task_types/<int:pk>/delete/",
        TaskTypeDeleteView.as_view(),
        name="task-type-delete",
    ),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/", update_completion, name = 'update-completion'),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("students/", StudentListView.as_view(), name="student-list"),
    path(
        "students/<int:pk>/", StudentDetailView.as_view(), name="student-detail"
    ),
    path("students/create/", StudentCreateView.as_view(), name="student-create"),
    path(
        "students/<int:pk>/update/",
        StudentGroupUpdateView.as_view(),
        name="student-update",
    ),
    path(
        "students/<int:pk>/delete/",
        StudentDeleteView.as_view(),
        name="student-delete",
    ),
]

app_name = "manager"
