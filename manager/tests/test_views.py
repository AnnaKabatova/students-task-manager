from datetime import datetime

import pytz
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from manager.models import Task, TaskType, Group, Student

TASK_URL = reverse("manager:task-list")
TASK_TYPE_URL = reverse("manager:task-type-list")
STUDENT_URL = reverse("manager:student-list")
GROUP_URL = reverse("manager:group-list")


class PublicTaskTests(TestCase):
    def test_list_login_required(self):
        res = self.client.get(TASK_URL)
        
        self.assertNotEqual(res.status_code, 200)


class PrivateTaskTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)
        
        europe_kiev = pytz.timezone('Europe/Kiev')
        self.task = Task.objects.create(
            name="Test Task",
            description="Test description",
            deadline=datetime(2024, 3, 5, 14, 30, tzinfo=europe_kiev),
            is_completed=False
        )
        self.url = reverse("manager:update-completion", kwargs={'pk': self.task.pk})
    
    def test_retrieve_tasks(self):
        Task(name="write an essay")
        Task(name="pass an exam")
        
        response = self.client.get(TASK_URL)
        
        tasks = Task.objects.all()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["task_list"]),
            list(tasks)
        )
        
        self.assertTemplateUsed(response, "manager/task_list.html")
    
    def test_for_update_task_completion(self):
        # Initial check if task is not completed
        self.assertFalse(self.task.is_completed)
        
        # Testing if task is marked as completed if it wasn't
        response = self.client.post(self.url)
        
        self.assertEqual(response.status_code, 200)
        
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_completed)
        
        # Check for "Undo" button to make task not completed
        response = self.client.post(self.url)
        
        self.assertEqual(response.status_code, 200)
        
        self.task.refresh_from_db()
        self.assertFalse(self.task.is_completed)


class PublicGroupTests(TestCase):
    def test_list_login_required(self):
        res = self.client.get(GROUP_URL)
        
        self.assertNotEqual(res.status_code, 200)


class PrivateGroupTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)
    
    def test_retrieve_groups(self):
        Group.objects.create(
            name="Test name"
        )
        
        response = self.client.get(GROUP_URL)
        
        groups = Group.objects.all()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["group_list"]),
            list(groups)
        )
        
        self.assertTemplateUsed(response, "manager/group_list.html")


class PublicTaskTypeTests(TestCase):
    def test_list_login_required(self):
        res = self.client.get(GROUP_URL)
        
        self.assertNotEqual(res.status_code, 200)


class PrivateTaskTypeTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)
    
    def test_retrieve_task_types(self):
        TaskType.objects.create(
            name="Test name"
        )
        
        response = self.client.get(TASK_TYPE_URL)
        
        types = TaskType.objects.all()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["task_type_list"]),
            list(types)
        )
        
        self.assertTemplateUsed(response, "manager/task_type_list.html")


class PublicStudentTests(TestCase):
    def test_list_login_required(self):
        res = self.client.get(STUDENT_URL)
        
        self.assertNotEqual(res.status_code, 200)


class PrivateStudentTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)
    
    def test_retrieve_students(self):
        Student.objects.create(
            username="Test username"
        )
        
        response = self.client.get(STUDENT_URL)
        
        student = Student.objects.all()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["student_list"]),
            list(student)
        )
        
        self.assertTemplateUsed(response, "manager/student_list.html")
