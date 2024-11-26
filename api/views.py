from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .models import Teacher, Student, TeacherStudentMapping, UserLogin,StudentSubject
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password,check_password
from django.db import IntegrityError

# Home view to render home.html
def home(request):
    return render(request, 'home.html')

# --- AUTHENTICATION VIEWS ---

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user_type = request.POST.get("usertype")  # 'student' or 'teacher'

        try:
            # Check UserLogin for the given username and user type
            user_login = UserLogin.objects.get(username=username, password=password, user_type=user_type)
            if user_type == "teacher":
                teacher = Teacher.objects.get(username=user_login.username)
                request.session['user_type'] = 'teacher'
                request.session['user_id'] = teacher.id
                messages.success(request, "Login successful!")
                return redirect('teacher_dashboard', teacher_id=teacher.id)
            elif user_type == "student":
                student = Student.objects.get(username=user_login.username)
                request.session['user_type'] = 'student'
                request.session['user_id'] = student.id
                messages.success(request, "Login successful!")
                return redirect('student_dashboard', student_id=student.id)
        except UserLogin.DoesNotExist:
            messages.error(request, f"Invalid credentials for {user_type}!")
        except (Teacher.DoesNotExist, Student.DoesNotExist):
            messages.error(request, f"{user_type.capitalize()} record not found!")

        return redirect('login')

    return render(request, "login.html")





def user_logout(request):
    logout(request)
    request.session.flush()
    messages.success(request, "You have been logged out.")
    return redirect('login')

# --- TEACHER VIEWS ---

@login_required
def teacher_dashboard(request,teacher_id):
    if request.session.get('user_type') != 'teacher':
        return redirect('login')
    teacher = get_object_or_404(Teacher, id=teacher_id)

    # Get the teacher instance
    teacher = Teacher.objects.get(id=teacher_id)
    
    # Get the number of students assigned to this teacher
    num_students_assigned = Student.objects.filter(teacher=teacher).count()

    # Pass the count to the template context
    context = {
        'teacher': teacher,
        'num_students_assigned': num_students_assigned,
    }

    return render(request, 'teacher_dashboard.html', context)


@login_required
def add_student_mapping(request):
    if request.method == "POST" and request.session.get('user_type') == 'teacher':
        student_id = request.POST.get('student_id')
        teacher_id = request.session.get('user_id')

        teacher = get_object_or_404(Teacher, id=teacher_id)
        student = get_object_or_404(Student, id=student_id)

        if TeacherStudentMapping.objects.filter(teacher=teacher, student=student).exists():
            messages.error(request, "Mapping already exists!")
        else:
            TeacherStudentMapping.objects.create(teacher=teacher, student=student)
            messages.success(request, "Student successfully added!")

        return redirect('teacher_dashboard')

    # Handle GET request (display form)
    students = Student.objects.all()
    return render(request, 'add_student_mapping.html', {'students': students})


@login_required
def remove_student_mapping(request, mapping_id):
    if request.session.get('user_type') != 'teacher':
        return redirect('login')

    mapping = get_object_or_404(TeacherStudentMapping, id=mapping_id)
    mapping.delete()
    messages.success(request, "Student removed successfully!")

    return redirect('teacher_dashboard')


# --- STUDENT VIEWS ---

@login_required
def student_dashboard(request, student_id):
    try:
        # Fetch the student details using the student_id from the URL
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        messages.error(request, "Student not found.")
        return redirect('login')

    context = {
        'student': student
    }

    return render(request, 'student_dashboard.html', context)
# --- ADMIN VIEWS (OPTIONAL) ---


# --- ADD STUDENT VIEW ---

@login_required
def add_student(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    
    if request.method == 'POST':
        # Collect data from the form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        blood_group = request.POST.get('blood_group')
        contact_number = request.POST.get('contact_number')
        address = request.POST.get('address')
        profile_pic = request.FILES.get('profile_pic')

        # Ensure required fields are filled
        if not first_name or not last_name or not date_of_birth:
            messages.error(request, "Please fill in all required fields.")
            return redirect('add_student', teacher_id=teacher.id)

        # Automatically generate username and password
        username = f"{first_name.lower()}_{last_name.lower()}"
        password = username  # Default password is the same as username

        # Check if the username already exists in UserLogin
        if UserLogin.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Please choose another one.")
            return redirect('add_student', teacher_id=teacher.id)

        try:
            # Create the Student instance and automatically assign the teacher and subject
            student = Student.objects.create(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                gender=gender,
                blood_group=blood_group,
                contact_number=contact_number,
                address=address,
                profile_pic=profile_pic,
                teacher=teacher,  # Assign the teacher to the student
                subject_name=teacher.subject  # This will be automatically set from the teacher's subject
            )

            # Create a corresponding UserLogin entry
            UserLogin.objects.create(
                username=username,
                password=password,
                user_type='student'  # Automatically set user type as 'student'
            )

            # Optional: If you have a TeacherStudentMapping, you can create it here
            # TeacherStudentMapping.objects.create(teacher=teacher, student=student)

            # Create the StudentSubject entry
            StudentSubject.objects.create(student=student, teacher=teacher)

            messages.success(request, "Student added successfully!")
            return redirect('teacher_dashboard', teacher_id=teacher.id)

        except Exception as e:
            # Handle errors gracefully
            messages.error(request, f"Error creating student record: {str(e)}")
            return redirect('add_student', teacher_id=teacher.id)

    return render(request, 'add_student.html', {'teacher': teacher})


@login_required
def teacher_profile(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)

    if request.method == 'POST':
        if 'update_profile' in request.POST:  # Handle profile update
            teacher.name = request.POST.get('name')
            teacher.subject = request.POST.get('subject')
            teacher.username = request.POST.get('username')
            teacher.save()
            messages.success(request, "Profile updated successfully.")

        elif 'change_password' in request.POST:  # Handle password change
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if new_password == confirm_password:
                teacher.password = new_password
                teacher.save()
                messages.success(request, "Password changed successfully.")
            else:
                messages.error(request, "Passwords do not match.")

        return redirect('teacher_profile', teacher_id=teacher.id)

    return render(request, 'teacher_profile.html', {'teacher': teacher})
def teacher_students(request, teacher_id):
    # Get the teacher object based on teacher_id
    teacher = get_object_or_404(Teacher, id=teacher_id)

    # Get all students who are associated with this teacher
    students = Student.objects.filter(teacher=teacher)

    # Render the student list page with teacher and student information
    return render(request, 'teacher_students.html', {'teacher': teacher, 'students': students})

@login_required
def update_student(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        messages.error(request, "Student not found.")
        return redirect('student_dashboard', student_id=student_id)
    
    if request.method == 'POST':
        # Update student fields manually
        student.first_name = request.POST.get('first_name', student.first_name)
        student.last_name = request.POST.get('last_name', student.last_name)
        student.date_of_birth = request.POST.get('date_of_birth', student.date_of_birth)
        student.gender = request.POST.get('gender', student.gender)
        student.blood_group = request.POST.get('blood_group', student.blood_group)
        student.contact_number = request.POST.get('contact_number', student.contact_number)
        student.address = request.POST.get('address', student.address)
        
        # Check if a new profile picture was uploaded
        if request.FILES.get('profile_pic'):
            student.profile_pic = request.FILES['profile_pic']
        
        # Save the updated student instance
        student.save()
        
        messages.success(request, "Your profile has been updated successfully.")
        return redirect('student_dashboard', student_id=student.id)
    
    return render(request, 'update_student.html', {'student': student})