from django.db import migrations
from django.db.migrations import RunPython


def func(apps, schema_editor):
    from django.core.management import call_command
    call_command('loaddata', 'fixture_data.json')


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("manager", "0003_alter_task_task_type"),
    ]
    
    operations = [RunPython(func, reverse_func)]
