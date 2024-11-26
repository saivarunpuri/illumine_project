from django.db import models

class UserLogin(models.Model):
    TYPE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )

    username = models.CharField(max_length=100, unique=True)  # Unique username for login
    password = models.CharField(max_length=100)  # Password
    user_type = models.CharField(max_length=10, choices=TYPE_CHOICES)  # Type: Student or Teacher

    def __str__(self):
        return f"{self.username} ({self.user_type})"

class Teacher(models.Model):
    
    name = models.CharField(max_length=100)  # Teacher name
    subject = models.CharField(max_length=100)  # Subject taught
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)  # Password (can be reused from UserLogin for simplicity)

    def __str__(self):
        return f"{self.name} ({self.subject})"
    def save(self, *args, **kwargs):
        # Automatically create a corresponding UserLogin record when saving the teacher
        if not self.username:  # Ensure a username is assigned before saving
            self.username = self.name.lower().replace(" ", "_")  # Example username generation
        if not self.password:  # Set a default password if none is provided
            self.password = "defaultpassword"  # You can modify this logic as per your requirements
        
        # Save the Teacher instance
        super().save(*args, **kwargs)

        # Ensure the corresponding UserLogin record exists
        user_login, created = UserLogin.objects.get_or_create(
            username=self.username,
            user_type='teacher',  # Since this is a teacher
            defaults={'password': self.password}  # Use the same password
        )

    # Ensure the Teacher's UserLogin is created or updated when saving the teacher
    def delete(self, *args, **kwargs):
        user_login = UserLogin.objects.filter(username=self.username, user_type='teacher')
        if user_login.exists():
            user_login.delete()
        super().delete(*args, **kwargs)

class Student(models.Model):
    username = models.CharField(max_length=100, unique=True, blank=True)
    password = models.CharField(max_length=128, blank=True)
    profile_pic = models.ImageField(upload_to='student_pics/', blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=(('male', 'Male'), ('female', 'Female')))
    blood_group = models.CharField(max_length=3)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()

    # New fields for teacher and subject
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    subject_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        # Assign default username and password if not provided
        if not self.username:
            self.username = self.first_name.lower() + "_" + self.last_name.lower()
        if not self.password:
            self.password = self.username  # Default password is the same as the username

        # If a teacher is assigned, set the subject_name automatically
        if self.teacher:
            self.subject_name = self.teacher.subject

        # Save the instance
        super().save(*args, **kwargs)

        # Ensure a corresponding UserLogin record exists
        user_login, created = UserLogin.objects.get_or_create(
            username=self.username,
            user_type='student',
            defaults={'password': self.password}
        )
        if not created:
            # Update password if it already exists
            user_login.password = self.password
            user_login.save()

    def delete(self, *args, **kwargs):
        # Delete the corresponding UserLogin record
        UserLogin.objects.filter(username=self.username, user_type='student').delete()
        super().delete(*args, **kwargs)


class StudentSubject(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Link to Student
    subject = models.CharField(max_length=100)  # Subject from Teacher table


    def __str__(self):
        return f"{self.student.student_name} - {self.teacher.subject}"
    
class TeacherStudentMapping(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.teacher.name} -> {self.student.first_name} {self.student.last_name}"
