# HRMS Lite - Backend

Production-ready Django REST API for Human Resource Management System.

## Features

- **Employee Management**: CRUD operations for employees
- **Attendance Tracking**: Mark and track daily attendance
- **Dashboard**: Statistics and summary views
- **Health Checks**: `/health/` and `/ready/` endpoints for monitoring

## Project Structure

```
backend/
├── hrms_lite/           # Project configuration
│   ├── settings/        # Split settings (base, development, production)
│   ├── exceptions.py    # Custom exception handlers
│   ├── pagination.py    # Pagination classes
│   ├── health.py        # Health check endpoints
│   └── urls.py          # Root URL configuration
├── hr/                  # Employee management app
├── attendance/          # Attendance tracking app
├── logs/               # Application logs
├── .env                # Environment variables (not in git)
├── .env.example        # Example environment file
├── manage.py           # Django CLI
└── requirements.txt    # Python dependencies
```

## Setup

### 1. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Start Development Server
```bash
python manage.py runserver 8000
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DJANGO_ENV` | Environment (development/production) | development |
| `SECRET_KEY` | Django secret key | - |
| `DEBUG` | Debug mode | True |
| `DATABASE_URL` | PostgreSQL connection URL | - |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | localhost |
| `CORS_ALLOWED_ORIGINS` | Comma-separated CORS origins | - |

## API Endpoints

### Employees
- `GET /api/employees/` - List all employees
- `POST /api/employees/` - Create employee
- `GET /api/employees/{id}/` - Get employee details
- `PUT /api/employees/{id}/` - Update employee
- `DELETE /api/employees/{id}/` - Delete employee
- `GET /api/employees/{id}/attendance/` - Get employee attendance

### Attendance
- `GET /api/attendance/` - List attendance records
- `POST /api/attendance/` - Mark attendance

### Dashboard
- `GET /api/dashboard/` - Get dashboard statistics

### Health
- `GET /health/` - Basic health check
- `GET /ready/` - Readiness check (with DB)

## Production Deployment

### Using Gunicorn
```bash
DJANGO_ENV=production gunicorn hrms_lite.wsgi:application --bind 0.0.0.0:8000
```

### Static Files
```bash
python manage.py collectstatic --noinput
```
