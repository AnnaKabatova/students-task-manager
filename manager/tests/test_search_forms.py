from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from manager.models import Student, Task


class TestSearch(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user"
        )
        self.client.force_login(self.user)
    
    def test_search_students_by_username(self):
        response = self.client.get(
            reverse("manager:student-list") + "?name=test_user"
        )
        self.assertEqual(
            list(response.context["student_list"]),
            list(Student.objects.filter(username__icontains="test_user")),
        )
    
    def test_search_task_by_name(self):
        response = self.client.get(
            reverse("manager:task-list") + "?name=write"
        )
        self.assertEqual(
            list(response.context["task_list"]),
            list(Task.objects.filter(name__icontains="write")),
        )
