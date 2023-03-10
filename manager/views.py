from typing import Optional, Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic, View
from django.http import HttpResponse

from .forms import *
from .models import TaskType, Group


def index(request) -> HttpResponse:
    """View function for the home page"""
    
    num_students = Student.objects.count()
    num_tasks = Task.objects.count()
    num_groups = Group.objects.count()
    
    context = {
        "num_students": num_students,
        "num_tasks": num_tasks,
        "num_groups": num_groups,
    }
    
    return render(request, "manager/index.html", context=context)


class StudentListView(LoginRequiredMixin, generic.ListView):
    model = Student
    paginate_by = 5
    
    def get_context_data(
            self,
            *,
            object_list: Optional[list[Any]] = None,
            **kwargs
    ) -> dict:
        context = super(StudentListView, self).get_context_data(**kwargs)
        
        username = self.request.GET.get("username", "")
        
        context["search_form"] = StudentSearchForm(initial={
            "username": username
        })
        
        return context
    
    def get_queryset(self) -> QuerySet:
        queryset = Student.objects.all()
        
        form = StudentSearchForm(self.request.GET)
        
        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        
        return queryset


class StudentDetailView(LoginRequiredMixin, generic.DetailView):
    model = Student
    queryset = Student.objects.prefetch_related("tasks__task_type").select_related("group")


class StudentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Student
    form_class = StudentCreationForm


class StudentGroupUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Student
    form_class = StudentGroupUpdateForm
    success_url = reverse_lazy("manager:student-list")


class StudentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Student
    success_url = reverse_lazy("manager:student-list")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "manager/task_list.html"
    paginate_by = 10
    
    def get_context_data(
            self,
            *,
            object_list: Optional[list[Any]] = None,
            **kwargs
    ) -> dict:
        context = super(TaskListView, self).get_context_data(**kwargs)
        
        name = self.request.GET.get("name", "")
        
        context["search_form"] = TaskSearchForm(initial={
            "name": name
        })
        
        return context
    
    def get_queryset(self) -> QuerySet:
        queryset = Task.objects.prefetch_related("assignees").select_related("task_type")
        
        form = TaskSearchForm(self.request.GET)
        
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        
        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.all()


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    success_url = reverse_lazy("manager:task-list")
    form_class = TaskForm


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    success_url = reverse_lazy("manager:task-list")
    form_class = TaskForm


class TaskUpdateCompletionView(LoginRequiredMixin, View):
    def get(self, request, pk) -> HttpResponse:
        task = Task.objects.get(id=pk)
        task.is_completed = not task.is_completed
        task.save()
        context = {
            "task": task
        }
        return render(request, "manager/task_detail.html", context=context)
    
    def post(self, request, pk) -> HttpResponse:
        task = Task.objects.get(id=pk)
        task.is_completed = request.POST.get("is_completed", not task.is_completed)
        task.save()
        context = {
            "task": task
        }
        return render(request, "manager/task_detail.html", context=context)


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("manager:task-list")


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    paginate_by = 4
    template_name = "manager/task_type_list.html"
    context_object_name = "task_type_list"


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    template_name = "manager/task_type_form.html"
    success_url = reverse_lazy("manager:task-type-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    template_name = "manager/task_type_form.html"
    success_url = reverse_lazy("manager:task-type-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    template_name = "manager/task_type_confirm_delete.html"
    success_url = reverse_lazy("manager:task-type-list")


class GroupListView(LoginRequiredMixin, generic.ListView):
    model = Group
    paginate_by = 4
    template_name = "manager/group_list.html"
    context_object_name = "group_list"


class GroupCreateView(LoginRequiredMixin, generic.CreateView):
    model = Group
    fields = "__all__"
    template_name = "manager/group_form.html"
    success_url = reverse_lazy("manager:group-list")


class GroupUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Group
    fields = "__all__"
    template_name = "manager/group_form.html"
    success_url = reverse_lazy("manager:group-list")


class GroupDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Group
    template_name = "manager/group_confirm_delete.html"
    success_url = reverse_lazy("manager:group-list")
