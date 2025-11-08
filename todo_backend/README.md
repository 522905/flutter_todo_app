# 🚀 Todo Backend API

Django REST API for the enhanced Flutter Todo application with notifications, WhatsApp/Email integration, and comprehensive task management.

## 📋 Features

- ✅ JWT Authentication
- ✅ Task CRUD operations
- ✅ Bulk task operations
- ✅ Email notifications
- ✅ WhatsApp notifications (Twilio)
- ✅ Push notifications (Firebase)
- ✅ Task analytics and history
- ✅ Scheduled reminders (Celery)
- ✅ API documentation (Swagger)

## 🛠️ Setup Instructions

### 1. Install Dependencies

```bash
cd todo_backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

### 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser

```bash
python manage.py createsuperuser
```

### 5. Run Development Server

```bash
python manage.py runserver
```

Server will run at: `http://localhost:8000`

### 6. Start Celery Worker (Optional - for notifications)

In a separate terminal:

```bash
# Start Redis (required for Celery)
redis-server

# Start Celery worker
celery -A config worker -l info

# Start Celery beat (for scheduled tasks)
celery -A config beat -l info
```

## 📚 API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login (get JWT tokens)
- `POST /api/auth/refresh/` - Refresh access token
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/` - Update user profile

### Tasks
- `GET /api/tasks/` - List all tasks (paginated, filterable)
- `POST /api/tasks/` - Create new task
- `GET /api/tasks/{id}/` - Get task detail
- `PUT /api/tasks/{id}/` - Update task
- `DELETE /api/tasks/{id}/` - Delete task
- `POST /api/tasks/{id}/complete/` - Mark task complete
- `POST /api/tasks/bulk-create/` - Bulk create tasks
- `POST /api/tasks/bulk-delete/` - Bulk delete tasks
- `POST /api/tasks/bulk-complete/` - Bulk mark complete

### Notifications
- `GET /api/notifications/` - List notifications
- `POST /api/notifications/send/` - Send notification
- `GET /api/notifications/history/` - Notification history

### Analytics
- `GET /api/analytics/stats/` - Task statistics
- `GET /api/analytics/history/` - Completion history

## 📖 API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **Admin Panel**: http://localhost:8000/admin/

## 🔧 Configuration

### Email Setup (Gmail)

1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Update `.env`:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### WhatsApp Setup (Twilio)

1. Sign up for Twilio: https://www.twilio.com/
2. Get WhatsApp sandbox credentials
3. Update `.env`:

```env
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
```

### Firebase Setup (Push Notifications)

1. Create Firebase project: https://console.firebase.google.com/
2. Download service account JSON
3. Update `.env`:

```env
FIREBASE_CREDENTIALS_PATH=/path/to/serviceAccountKey.json
```

## 🧪 Testing

```bash
python manage.py test
```

## 📦 Project Structure

```
todo_backend/
├── config/              # Project settings
│   ├── settings.py      # Django settings
│   ├── urls.py          # Root URLs
│   └── celery.py        # Celery config
├── users/               # User management
├── tasks/               # Task CRUD
├── notifications/       # Notification system
├── analytics/           # Analytics & stats
├── manage.py
└── requirements.txt
```

## 🚀 Deployment

### Using Railway/Render

1. Connect your GitHub repository
2. Set environment variables
3. Deploy!

### Using Docker

```bash
docker-compose up -d
```

## 📝 License

MIT License
