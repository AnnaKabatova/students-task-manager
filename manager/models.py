from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class TaskType(models.Model):
    name = models.CharField(max_length=63, unique=True)
    
    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name


class Student(AbstractUser):
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name = "student"
        verbose_name_plural = "students"
    
    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"
    
    def get_absolute_url(self):
        return reverse("manager:student-detail", kwargs={"pk": self.pk})


class Task(models.Model):
    PRIORITY_CHOICES = (
        ("URGENT", "Urgent"),
        ("HIGH", "High"),
        ("LOW", "Low"),
        ("OPTIONAL", "Optional"),
    )
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(null=True, default=False)
    priority = models.CharField(max_length=9, choices=PRIORITY_CHOICES, default="HIGH")
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE, null=True)
    assignees = models.ManyToManyField(Student, related_name="tasks")
    
    def __str__(self):
        return self.name
