# Generated by Django 5.1.3 on 2024-11-25 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_student_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='username',
            new_name='user_login',
        ),
        migrations.RemoveField(
            model_name='student',
            name='password',
        ),
    ]
