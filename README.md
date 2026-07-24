# QueryLab

## Overview

QueryLab is a Django-based web application for learning SQL through two complementary workflows: guided theory-and-quiz study and hands-on SQL practice. Users can browse SQL topics, read explanations, answer multiple-choice questions, review their progress on a personal dashboard, and run SQL queries against practice datasets inside the application.

The main goal of the project is to turn SQL study into an interactive experience instead of a static reading experience. Rather than only presenting definitions and syntax examples, QueryLab gives users a place to immediately apply what they are learning. The application combines topic summaries, question-based reinforcement, progress tracking, and practical SQL exercises in a single interface.

From the user perspective, the workflow is straightforward. A user creates an account, logs in, studies a topic, answers questions, then goes to the Lab to attempt SQL exercises. Practice exercises are evaluated dynamically by building temporary SQLite databases from structured JSON datasets and comparing the result of the user query with the expected result.

The project was designed to offer a cleaner and more engaging study experience, combining educational content with direct experimentation. Generative AI was also used as a support tool during interface refinement, helping improve layout decisions, presentation clarity, and the overall visual experience while keeping the application structure and back-end logic implemented in Django and JavaScript.

## Distinctiveness and Complexity

QueryLab is focused on SQL education and practice. Its core value is structured learning content combined with dynamic query evaluation, allowing users to move between theory, quizzes, and hands-on exercises in the same environment. The application is centered on a domain-specific study flow built to make SQL learning active and measurable.

The project combines several features into one coherent application. It includes authentication, database-backed content organization, user-specific progress tracking, asynchronous quiz submission, a dashboard with calculated statistics, and a lab system that evaluates SQL practice submissions. The SQL practice component is especially important: instead of simply storing text answers, the app builds in-memory SQLite databases from JSON data, executes SQL statements, and compares the output of the user query to the expected output.

Another reason the project is sufficiently complex is that it requires both Django and front-end JavaScript in meaningful ways. Django is responsible for routing, models, authentication, persistence, and practice evaluation. JavaScript is used on the front end to fetch topic details dynamically, render quizzes without a full page reload, submit answers asynchronously, and update feedback in the interface. In other words, the application is not just a server-rendered site with minimal scripts; it uses JavaScript to deliver interactive learning behavior.

Finally, the application has more than one type of user interaction and more than one type of learning surface. A user can read theory, answer quiz questions, review personal performance on a dashboard, and attempt SQL practice exercises. These pieces interact with each other through models such as topics, questions, choices, answers, practices, and submissions. That combination of learning content, user progress, and SQL execution gives the platform both educational depth and technical variety.

## Main Features

- User registration and authentication.
- Topic browsing with summaries and theory sections.
- Dynamic question loading for each topic using JavaScript and fetch.
- Asynchronous answer submission with instant feedback.
- Progress dashboard showing accuracy, completion, and per-topic performance.
- Practice Lab listing SQL exercises either globally or by topic.
- SQL practice evaluation using temporary in-memory SQLite databases.
- Storage of user practice submissions and correctness state.
- Password reset pages through Django authentication templates.
- Mobile-friendly layout based on Bootstrap.

## Technologies Used

- Python
- Django
- SQLite
- JavaScript
- HTML
- CSS
- Bootstrap 5
- Generative AI for interface refinement and UX ideation
- django-crispy-forms
- crispy-bootstrap5

## Project Structure

### Root Files

- `manage.py`: Django management entry point.
- `db.sqlite3`: local SQLite database used during development.

### Project Configuration

- `sql_study_hub/settings.py`: Django settings, installed apps, static files, authentication redirects, and email configuration.
- `sql_study_hub/urls.py`: root URL configuration for the project.
- `sql_study_hub/asgi.py` and `sql_study_hub/wsgi.py`: ASGI and WSGI entry points.

### Main Application

- `study_hub/models.py`: application models, including the custom user model, topics, quiz questions, choices, user answers, practice exercises, and practice submissions.
- `study_hub/views.py`: all main view logic, including registration, dashboard, topic JSON responses, quiz submission, lab listing, and SQL practice evaluation.
- `study_hub/urls.py`: application-specific routes such as home, dashboard, practice routes, and answer submission endpoints.
- `study_hub/admin.py`: admin registration for application models.
- `study_hub/tests.py`: placeholder for tests.

### Templates

- `study_hub/templates/study_hub/layout.html`: base layout and navigation.
- `study_hub/templates/study_hub/index.html`: landing page for SQL topics.
- `study_hub/templates/study_hub/topics_list.html`: topic list partial used on the home page.
- `study_hub/templates/study_hub/dashboard.html`: user progress dashboard.
- `study_hub/templates/study_hub/register.html`: registration page.
- `study_hub/templates/study_hub/practice_list.html`: lab page listing practice exercises.
- `study_hub/templates/study_hub/practice.html`: individual SQL practice page.
- `templates/registration/login.html`: login page.
- `templates/registration/password_reset_form.html`: password reset request page.
- `templates/registration/password_reset_done.html`: confirmation that reset email was sent.
- `templates/registration/password_reset_confirm.html`: password reset confirmation form.
- `templates/registration/password_reset_complete.html`: reset completion page.

### Static Files

- `study_hub/static/study_hub/index.js`: front-end JavaScript for dynamic topic loading and asynchronous question submission.
- `study_hub/static/study_hub/styles.css`: custom styling on top of Bootstrap.

### Data and Migrations

- `study_hub/management/commands/seed_data.py`: custom management command that seeds topics, quiz questions, choices, and SQL practice exercises.
- `study_hub/migrations/`: migration history for the application database schema.

## Models

The app uses multiple Django models. `Topics` stores the subject areas for SQL learning. `Questions` and `Choices` define quiz content connected to a topic. `UserAnswer` stores each user’s answer and whether it was correct, which is later used for dashboard metrics.

For the lab system, `PracticeExercise` stores the instructions, expected SQL query, and JSON dataset used to create a temporary database. `PracticeSubmission` stores each user submission and whether the evaluated result was correct. This allows the Lab feature to behave differently from the quiz feature while still keeping user progress in the database.

## How the SQL Practice System Works

Each practice exercise stores a dataset as JSON. When a user submits a query, the server builds temporary SQLite databases in memory. One database is used to execute the expected query, and another is used to execute the user query. Since both start from the same initial data, the comparison is isolated and does not depend on previous attempts. This design allows users to retry practices multiple times without permanently changing the base dataset for the exercise.

This practice flow is one of the main reasons the application is more complex than a basic content site. It goes beyond storing answers in a table and instead evaluates SQL against controlled data on demand.

## How to Run the Application

1. Make sure Python is installed.
2. Create and activate a virtual environment if desired.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply migrations:

```bash
python manage.py migrate
```

5. Seed the database with topics, questions, and practice exercises:

```bash
python manage.py seed_data
```

6. Start the development server:

```bash
python manage.py runserver
```

7. Open the application in the browser at:

```text
http://127.0.0.1:8000/
```

## Deploy on Railway

The project is now structured so sensitive settings can be provided through environment variables instead of being hard-coded in the repository. This makes it suitable for deployment through GitHub + Railway.

### Production configuration used by the project

The Django settings support:

- `SECRET_KEY` loaded from environment variables.
- `DEBUG=False` in production.
- `ALLOWED_HOSTS` loaded from environment variables.
- Automatic support for `RAILWAY_PUBLIC_DOMAIN`.
- `DATABASE_URL` for a managed database on Railway, with SQLite still available as a local fallback.
- Email credentials loaded from environment variables.
- Static file serving with WhiteNoise.

### Basic Railway deployment flow

1. Push the project to a GitHub repository.
2. Create a new project on Railway.
3. Choose `Deploy from GitHub repo` and connect the repository.
4. Add a PostgreSQL database in Railway if you want a production database instead of SQLite.
5. In Railway, open the service variables and add the required environment variables, such as:

```text
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app-name.up.railway.app
CSRF_TRUSTED_ORIGINS=https://your-app-name.up.railway.app
DATABASE_URL=postgresql://...
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-email-password-or-app-password
DEFAULT_FROM_EMAIL=your-email
```

6. Set the start command to run the Django app with Gunicorn:

```bash
gunicorn sql_study_hub.wsgi
```

7. During deployment, run migrations:

```bash
python manage.py migrate
```

8. If you want the initial content in production as well, run:

```bash
python manage.py seed_data
```

9. After the deployment finishes, open the Railway-generated domain to access the application.

### Notes for Railway

- The repository now includes the dependencies needed for Gunicorn, WhiteNoise, and `DATABASE_URL` parsing.
- If Railway exposes `RAILWAY_PUBLIC_DOMAIN`, the project can automatically accept that host.
- A managed PostgreSQL instance is the better long-term option for production.
- If the secret key or email password was previously committed to Git history, rotate those credentials before going live.

## How to Use the Application

- Register a new account or log in.
- Browse SQL topics from the home page.
- Click a topic to load theory and multiple-choice questions dynamically.
- Answer questions and receive instant feedback.
- Visit the dashboard to review progress statistics.
- Open the Lab section to browse practice exercises.
- Submit SQL queries in the practice page and compare your result with the expected result.

## Additional Information

The application uses a custom user model (`study_hub.User`), so migrations should always be run with that model in place. The project also includes Django password reset templates. In a real deployment, email credentials and other sensitive settings should be moved out of source code and stored in environment variables.

The current project is designed for local development using SQLite. The seeded practice exercises cover multiple SQL concepts such as `SELECT`, `WHERE`, `ORDER BY`, `DISTINCT`, `LIMIT`, `GROUP BY`, `HAVING`, joins, subqueries, and data modification commands. The Lab system is intended to reinforce the same concepts presented in the topic and quiz sections.

If I were continuing the project, the next improvements would be adding a stronger automated grading strategy for state-changing queries, expanding the dashboard with more detailed submission history, and increasing test coverage in `tests.py`.