from datetime import datetime

import pytz
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from manager.forms import StudentCreationForm, TaskForm
from manager.models import Group, TaskType


class FormsTests(TestCase):
    def test_student_creation_form_with_attributes_is_valid(self):
        group = Group.objects.create(name="test group")
        form_data = {
            "username": "new_user",
            "password1": "user123test",
            "password2": "user123test",
            "group": group,
            "first_name": "Test first",
            "last_name": "Test last",
        }
        form = StudentCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class PrivateStudentTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)
    
    def test_create_student(self):
        form_data = {
            "username": "new_user",
            "group": "test_group",
            "first_name": "Test first",
            "last_name": "Test last",
            "password1": "user123test",
            "password2": "user123test",
        }
        self.client.post(reverse("manager:student-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])
        
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])


class PrivateTaskFormTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)
    
    def test_valid_form(self):
        europe_kiev = pytz.timezone('Europe/Kiev')
        task_type = TaskType.objects.create(name="test task type")
        form_data = {
            "name": "test name",
            'description': 'test description',
            'deadline': datetime(2033, 8, 31, 0, 0, tzinfo=europe_kiev),
            "tags": task_type,
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
