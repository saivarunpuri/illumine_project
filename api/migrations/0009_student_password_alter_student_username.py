# Generated by Django 5.1.3 on 2024-11-25 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_rename_user_login_student_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='password',
            field=models.CharField(default='defaultpassword', max_length=128),
        ),
        migrations.AlterField(
            model_name='student',
            name='username',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
