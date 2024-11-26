
# Register your models here.
from django.contrib import admin
from .models import Teacher

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'username')  # Display teacher details
    search_fields = ('name', 'subject')  # Allow search for teachers
