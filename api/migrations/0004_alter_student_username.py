# Generated by Django 5.1.3 on 2024-11-25 14:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_student_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='username',
            field=models.OneToOneField(limit_choices_to={'user_type': 'student'}, on_delete=django.db.models.deletion.CASCADE, to='api.userlogin'),
        ),
    ]
