from datetime import datetime

import pytz
from django.contrib.auth import get_user_model
from django.test import TestCase

from manager.models import Task, TaskType, Group, Student


class ModelsTests(TestCase):
    def test_task_type_str(self):
        task_type = TaskType.objects.create(name="test")
        self.assertEqual(str(task_type), f"{task_type.name}")

    def test_group_str(self):
        group = Group.objects.create(name="test")
        self.assertEqual(str(group), f"{group.name}")

    def test_task_str(self):
        europe_kiev = pytz.timezone('Europe/Kiev')
        task = Task.objects.create(
            name="test name",
            description="test description",
            priority="test",
            deadline=datetime(2024, 3, 5, 14, 30, tzinfo=europe_kiev),
        )
        self.assertEqual(str(task), f"{task.name}")

    def test_student_str(self):
        student = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            first_name="Test first",
            last_name="Test last"
        )
        self.assertEqual(
            str(student),
            f"{student.username} ({student.first_name} {student.last_name})"
        )
