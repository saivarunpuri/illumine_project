# Generated by Django 5.1.3 on 2024-11-25 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_student_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='username',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
