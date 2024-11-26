
# College Management System

A web application built using Django to manage students and faculties at a college. The application provides access to two types of users: **Faculty** and **Student**, each with their own respective features and functionalities.

## Features

### Faculty Features:
- **Login:** Faculties can log in to the system.
- **Create Students:** Faculties can add new student profiles.
- **View All Students:** Faculties can view the list of all students.
- **Assign Students to Faculty:** Faculties can assign students to themselves.
- **Update Student Details:** Faculties can update student details.

### Student Features:
- **Login:** Students can log in to the system.
- **View Profile:** Students can view their profile, which includes:
  - Profile Picture
  - First Name
  - Last Name
  - Date of Birth
  - Gender
  - Blood Group
  - Contact Number
  - Address
- **Edit Profile:** Students can edit their profile details.
- **View Subjects and Related Faculties:** Students can view the subjects they are enrolled in, along with the respective faculty teaching the subject.

## Functional Requirements

- A **Faculty** can teach multiple students and handle their details.
- A **Faculty** can only teach one subject.
- A **Student** can be enrolled in multiple subjects.
- Proper **CRUD operations** (Create, Read, Update, Delete) are implemented for student and faculty management.
- The application gives **feedback** to users on CRUD operations.
- The **UI** is created using Django templates.

## Tech Stack

- **Backend:** Django (with templates)
- **Database:** PostgreSQL
- **UI:** Django Templates (with custom HTML/CSS for UI)
- **Authentication:** Django Authentication (for login functionality)

## Getting Started

### Prerequisites

Before running the application, make sure you have the following installed:

- **Python 3.x** (for Django backend)
- **PostgreSQL** (for database management)
- **Django** (backend framework)
- **Django Rest Framework** (optional for API usage)

### Setup Instructions

#### Backend (Django)

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <project-folder>
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up PostgreSQL for the project:
   - Create a PostgreSQL database and user for the application.
   - Update the `DATABASES` configuration in `settings.py` with your PostgreSQL credentials.

   Example:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'college_management',
           'USER': 'your_username',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

5. Apply migrations to set up the database:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser to access the Django admin and manage faculty and students:
   ```bash
   python manage.py createsuperuser
   ```

7. Start the Django server:
   ```bash
   python manage.py runserver
   ```

   Your backend should now be running at `http://127.0.0.1:8000`.

#### Django Admin

- Faculty users can be added through the Django admin interface at `http://127.0.0.1:8000/admin`.
- From there, you can manage faculties, students, subjects, and their relationships.

### Project Structure

```
college-management-system/
├── manage.py
├── college_mgmt/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── student_dashboard.html
│   │   ├── faculty_dashboard.html
│   └── static/
├── api/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── serializers.py
├── requirements.txt
└── README.md
```

## Feedback and CRUD Operations

- The application will provide feedback to users after performing CRUD operations, such as creating, updating, or deleting student profiles.
- Appropriate error messages and success alerts will be shown based on the user's actions.

## Contributing

If you'd like to contribute to the development of this project, feel free to fork the repository, create a branch, and submit a pull request.

---
