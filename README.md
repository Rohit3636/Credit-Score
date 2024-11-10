# Credit Bureau Update System

## Overview
This project is designed to build a dynamic credit bureau update system where users can interact through a series of questions, respond using a pop-up interface, and get their credit score calculated based on predefined algorithms. The entire system is implemented using Django, with modern front-end enhancements for user interaction. This project is hosted on [techturko.com](http://techturko.com).

## Features
- **User Authentication**: Secure user login/logout system.
- **Dynamic Question Rendering**: Questions pulled from the database and displayed in a modal interface.
- **Credit Score Calculation**: An algorithm that evaluates user responses and calculates their credit score.
- **Responsive Interface**: A dashboard that displays past scores and a modal for answering questions.

## Directory Structure
```plaintext
.
├── CreditScore/
│   ├── migrations/
│   ├── static/
│   │   ├── css/
│   │   │   └── main.css
│   │   ├── js/
│   │   │   └── main.js
│   ├── templates/
│   │   ├── CreditScore/
│   │   │   ├── dashboard.html
│   │   │   └── login.html
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── static/
│   ├── login.css
│   └── main.css
├── manage.py
└── TEST/
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

## Environments

### Local Environment
- **Database**: Uses `SQLite3` for ease of setup and testing.
- **Settings**: Default settings suitable for local development (`DEBUG = True`).
- **Static Files**: Static files served through Django for testing purposes.
- **Sensitive Information**: The secret key is exposed for local testing convenience. **Never use this key in production**.

### Production Environment
- **Database**: Configured to use MySQL. Ensure `mysqlclient==2.1.1` is added to the `requirements.txt`.
- **Settings Changes**:
  - **DEBUG**: Set to `False` for production.
  - **Allowed Hosts**: Add `ALLOWED_HOSTS = ['techturko.com']` to specify allowed domains.
  - **Secret Key**: The secret key should be kept hidden and securely retrieved from environment variables or a secure file.
  - **Static Files**: Use `python manage.py collectstatic` to gather all static assets for efficient serving.
  - **Database Credentials**: Store database credentials in environment variables to prevent exposure.

### Project Configuration (`settings.py`)
- Configures the Django project with essential settings like `INSTALLED_APPS`, `MIDDLEWARE`, and `DATABASES`.
- **For Production**:
  - Set `DEBUG = False`.
  - Update `DATABASES` to use MySQL.
  - Secure sensitive information such as the `SECRET_KEY` and database login credentials.
  - Ensure `ALLOWED_HOSTS` includes the production domain (`techturko.com`).

## Commands Overview
Below are essential commands for managing and deploying the project:

### Local Development Commands
- **Run Server**: Start the local development server.
  ```bash
  python manage.py runserver
  ```
- **Make Migrations**: Create migration files for any changes in models.
  ```bash
  python manage.py makemigrations
  ```
- **Apply Migrations**: Apply migrations to the database.
  ```bash
  python manage.py migrate
  ```
- **Create Superuser**: Create an admin user to access the Django admin panel.
  ```bash
  python manage.py createsuperuser
  ```
- **Install Requirements**: Install project dependencies from `requirements.txt`.
  ```bash
  pip install -r requirements.txt
  ```
- **Virtual Environment (venv)**: Create and activate a virtual environment to isolate dependencies.
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows use `venv\Scripts\activate`
  ```

### Production Commands
- **Collect Static Files**: Gather all static files in one directory for efficient serving in production.
  ```bash
  python manage.py collectstatic
  ```
- **Start Server with WSGI**: Use a WSGI server like `gunicorn` to serve the Django application in production.
  ```bash
  gunicorn TEST.wsgi:application --bind 0.0.0.0:8000
  ```

### Additional Notes
- **Virtual Environment**: It is recommended to use a virtual environment to avoid conflicts between dependencies across different projects.
- **Database Management**: In the production environment, be sure to create a robust backup strategy for the MySQL database.
- **Logging**: In production, set up proper logging for both error and access logs to track the application's health.

## Detailed Explanation

### URL Patterns (`urls.py`)
- Routes to views such as login, logout, home, and form submission.
- Admin panel customization with `admin.site.site_header`, `admin.site.site_title`, and `admin.site.index_title` for a branded admin interface.

### Models (`models.py`)
#### UserProfile Model
- Extends the Django `User` model to include email and company details.
- Used for tracking user-specific data across responses and scores.

#### Question Model
- Stores questions displayed to the user.
- Related to the `Option` model, which links possible answers with respective weightages for scoring.

#### Option Model
- Holds the answer options for each question with an associated weightage.
- Critical for calculating scores based on user responses.

#### UserResponse Model
- Captures each response a user submits, linking the `UserProfile`, `Question`, and chosen `Option`.

#### CreditScore Model
- Records the final credit score for each user session, along with a timestamp.

### Views (`views.py`)
- **`loginPage()`**: Handles user authentication. Validates user credentials and displays appropriate messages for success or failure.
- **`logout_view()`**: Logs out the user and redirects them to the login page.
- **`home()`**: Fetches and displays questions with options and shows a history of the user's credit scores.
- **`submit_responses()`**: Processes and validates responses, calculates the total score, caps it at 900, and records it in the database.

### Admin Customization (`admin.py`)
- Custom admin configuration for managing `Question`, `Option`, `UserProfile`, and `CreditScore`.
- Inlines `Option` in `QuestionAdmin` to allow seamless option management during question edits.

### Front-End Templates
#### `dashboard.html`
- Implements a modal interface for dynamic question display.
- Features a table to list previous credit scores.
- Includes Bootstrap for responsiveness and animations for a modern UX.

#### `login.html`
- Provides a login form with Bootstrap styling and Django messaging for feedback.
- Simple and clean UI for user authentication.

### JavaScript Functionality
- Dynamically populates questions and options using JSON data.
- Manages question navigation and final form submission through AJAX.

## How It Works
1. **User Logs In**: The `loginPage()` view authenticates the user.
2. **Dashboard Display**: The `home()` view renders the `dashboard.html` template, loading questions and past scores.
3. **Answer Submission**: Users submit answers via the modal, processed by `submit_responses()`, which calculates and stores the credit score.
4. **Result Display**: The updated credit score appears in the modal and is recorded in the database.

## Project Dependencies
- **Django**: Core web framework.
- **Bootstrap**: Styling and responsive design.
- **jQuery**: Assists with form interactions.
- **CSRF Protection**: Ensures secure form submissions.
- **mysqlclient**: Required for MySQL database integration in production.

## Future Enhancements
- Integrate additional scoring criteria or complex algorithms.
- Expand with user notifications and improved score analytics.
- Enhance security with user input validation and stricter session management.

