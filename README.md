# Josh-Backed-Task
Task management System

# Task Management API

## Project Overview
This is a Django-based task management application that allows users to create tasks, assign tasks to users, and retrieve tasks for specific users.

## Project Setup

### Prerequisites
- Python 3.8+
- pip
- virtualenv (recommended)

### Installation Steps
1. Clone the repository
```bash
git clone <repository-url>
cd task_management
```

2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up the database
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser
```bash
python manage.py createsuperuser
```

6. Run the development server
```bash
python manage.py runserver
```

## API Endpoints

### Create a Task
- **URL:** `/api/tasks/`
- **Method:** POST
- **Request Body:**
```json
{
  "name": "Task 2 - Prepare Demo",
  "description": "This is a task to configure DB",
  "task_type": "development"
}
```

### Assign Task to User
- **URL:** `/api/tasks/<task_id>/assign/`
- **Method:** POST
- **Request Body:**
```json
{
    "user_ids": [3, 4]
}
```
- **Response:**
```json
{
    "message": "Task assigned to 2 users",
    "task": {
        "id": 2,
        "name": "Task 2 - Prepare Demo",
        "description": "This is a task to configure DB",
        "created_at": "2025-03-25T18:25:41.776952Z",
        "completed_at": null,
        "task_type": "development",
        "status": "not_started",
        "assigned_users": [
            {
                "id": 3,
                "username": "vaibhavsingh",
                "email": ""
            },
            {
                "id": 4,
                "username": "AnandChow",
                "email": ""
            }
        ]
    }
}
```


### Get Tasks for a User
- **URL:** `/api/users/<user_id>/tasks/`
- **Method:** GET
- **Response:**
```json
[
    {
        "id": 1,
        "name": "Task 1 - Prepare Demo",
        "description": "This is a new task to prepare Demo",
        "created_at": "2025-03-25T18:15:56.490968Z",
        "completed_at": null,
        "task_type": "development",
        "status": "not_started",
        "assigned_users": [
            {
                "id": 2,
                "username": "shivamgovind",
                "email": ""
            },
            {
                "id": 3,
                "username": "vaibhavsingh",
                "email": ""
            }
        ]
    },
    {
        "id": 2,
        "name": "Task 2 - Prepare Demo",
        "description": "This is a task to configure DB",
        "created_at": "2025-03-25T18:25:41.776952Z",
        "completed_at": null,
        "task_type": "development",
        "status": "not_started",
        "assigned_users": [
            {
                "id": 3,
                "username": "vaibhavsingh",
                "email": ""
            },
            {
                "id": 4,
                "username": "AnandChow",
                "email": ""
            }
        ]
    }
]
```

## Test Credentials
- **Admin Username:** yashagrahari
- **Admin Password:** Yash@123