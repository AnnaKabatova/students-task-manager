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
