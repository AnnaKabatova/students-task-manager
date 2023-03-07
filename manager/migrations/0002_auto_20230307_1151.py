from django.db import migrations
from django.db.migrations import RunPython


def func(apps, schema_editor):
    from django.core.management import call_command
    call_command('loaddata', 'fixture_data.json')


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("manager", "0001_initial"),
        ("sessions", "0001_initial"),
    ]

    operations = [
        RunPython(func, reverse_func)
    ]
