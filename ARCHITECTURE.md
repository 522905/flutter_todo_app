# 📋 Enhanced Todo App - Architecture Documentation

## System Overview

A full-stack task management application with Flutter frontend and Django backend, featuring real-time notifications, WhatsApp/Email integration, and comprehensive task management.

---

## 🏗️ Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     FLUTTER MOBILE APP                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   UI Layer   │  │ State Mgmt   │  │  Local DB    │     │
│  │  (Widgets)   │──│  (Provider)  │──│   (Hive)     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                               │
│         └──────────────────┴─────────────────┐             │
│                                               │             │
│  ┌────────────────────────────────────────────┴──────────┐ │
│  │              SERVICES LAYER                            │ │
│  │  • API Service (HTTP Client)                          │ │
│  │  • Notification Service (Local + FCM)                 │ │
│  │  • Auth Service (JWT Token Management)                │ │
│  │  • Sync Service (Offline-first)                       │ │
│  └────────────────────────────────────────────────────────┘ │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTPS / REST API
                         │
┌────────────────────────┴────────────────────────────────────┐
│                    DJANGO BACKEND                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                  API LAYER (DRF)                     │   │
│  │  • Authentication API (JWT)                          │   │
│  │  • Tasks API (CRUD + Bulk)                          │   │
│  │  • Notifications API                                 │   │
│  │  • Analytics API                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                         │                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              BUSINESS LOGIC LAYER                    │   │
│  │  • Task Manager                                      │   │
│  │  • Notification Manager                              │   │
│  │  • User Manager                                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                         │                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                 DATA LAYER                           │   │
│  │  • PostgreSQL/SQLite (Main DB)                      │   │
│  │  • Redis (Celery Queue + Cache)                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │            ASYNC WORKERS (Celery)                    │   │
│  │  • Email Notification Task                           │   │
│  │  • WhatsApp Notification Task                        │   │
│  │  • Push Notification Task                            │   │
│  │  • Scheduled Reminders                               │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────┬────────────────┬──────────────────────────┘
                  │                │
         ┌────────┴────────┐  ┌────┴─────────┐
         │  SMTP Server    │  │  WhatsApp    │
         │  (Email)        │  │  Business    │
         │                 │  │  API         │
         └─────────────────┘  └──────────────┘
```

---

## 📱 Flutter App Architecture

### Tech Stack
- **Framework**: Flutter 3.x
- **State Management**: Provider
- **Local Database**: Hive
- **HTTP Client**: Dio
- **Authentication**: JWT
- **Notifications**:
  - flutter_local_notifications (Local)
  - firebase_messaging (Push)
- **UI**: Material Design 3

### Folder Structure
```
lib/
├── main.dart
├── models/
│   ├── user.dart
│   ├── task.dart
│   └── notification.dart
├── providers/
│   ├── auth_provider.dart
│   ├── task_provider.dart
│   └── notification_provider.dart
├── services/
│   ├── api_service.dart
│   ├── auth_service.dart
│   ├── notification_service.dart
│   └── sync_service.dart
├── screens/
│   ├── auth/
│   │   ├── login_screen.dart
│   │   └── signup_screen.dart
│   ├── home/
│   │   └── home_screen.dart
│   ├── tasks/
│   │   ├── task_list_screen.dart
│   │   ├── task_detail_screen.dart
│   │   ├── add_task_screen.dart
│   │   └── bulk_task_screen.dart
│   └── settings/
│       └── settings_screen.dart
├── widgets/
│   ├── task_card.dart
│   ├── priority_badge.dart
│   ├── category_chip.dart
│   └── custom_button.dart
├── utils/
│   ├── constants.dart
│   ├── themes.dart
│   └── helpers.dart
└── data/
    └── local_database.dart
```

### Key Features

#### 1. **Modern UI/UX**
- Gradient backgrounds with modern color schemes
- Card-based task layout
- Bottom navigation
- Smooth animations
- Dark/Light theme support
- Haptic feedback

#### 2. **Task Management**
- Create, read, update, delete tasks
- Task categories (Work, Personal, Shopping, etc.)
- Priority levels (High, Medium, Low)
- Due dates with reminders
- Subtasks support
- Task notes/description
- Bulk operations (create, delete, mark complete)

#### 3. **Notifications**
- Local scheduled notifications
- Push notifications from backend
- Customizable reminder times
- Notification badges

#### 4. **Integrations**
- Share tasks via WhatsApp
- Email task summaries
- Calendar integration (future)

#### 5. **Offline Support**
- Local-first architecture
- Auto-sync when online
- Conflict resolution

---

## 🔧 Django Backend Architecture

### Tech Stack
- **Framework**: Django 4.x + Django REST Framework
- **Database**: PostgreSQL (production) / SQLite (dev)
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Task Queue**: Celery
- **Message Broker**: Redis
- **Email**: Django Email Backend (SMTP)
- **WhatsApp**: Twilio API
- **Push Notifications**: Firebase Admin SDK

### Project Structure
```
todo_backend/
├── manage.py
├── requirements.txt
├── .env.example
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── celery.py
├── apps/
│   ├── users/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── tasks/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── services.py
│   ├── notifications/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── tasks.py (Celery tasks)
│   │   └── services/
│   │       ├── email_service.py
│   │       ├── whatsapp_service.py
│   │       └── push_service.py
│   └── analytics/
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       └── urls.py
└── utils/
    ├── permissions.py
    ├── pagination.py
    └── exceptions.py
```

### Database Models

#### User Model (Extended)
```python
class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True)
    fcm_token = models.CharField(max_length=255, blank=True)
    email_notifications = models.BooleanField(default=True)
    whatsapp_notifications = models.BooleanField(default=False)
    push_notifications = models.BooleanField(default=True)
```

#### Task Model
```python
class Task:
    - id (UUID)
    - user (ForeignKey)
    - title (CharField)
    - description (TextField)
    - category (CharField with choices)
    - priority (CharField: HIGH, MEDIUM, LOW)
    - is_completed (BooleanField)
    - due_date (DateTimeField)
    - reminder_time (DateTimeField)
    - created_at, updated_at
    - deleted_at (soft delete)
```

#### Notification Model
```python
class Notification:
    - id
    - user (ForeignKey)
    - task (ForeignKey)
    - type (EMAIL, WHATSAPP, PUSH)
    - status (PENDING, SENT, FAILED)
    - scheduled_at
    - sent_at
    - message
```

### API Endpoints

#### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login (returns JWT)
- `POST /api/auth/refresh/` - Refresh JWT token
- `POST /api/auth/logout/` - Logout
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/` - Update profile

#### Tasks
- `GET /api/tasks/` - List all tasks (with filters)
- `POST /api/tasks/` - Create task
- `GET /api/tasks/{id}/` - Get task detail
- `PUT /api/tasks/{id}/` - Update task
- `DELETE /api/tasks/{id}/` - Delete task
- `POST /api/tasks/bulk/` - Bulk create tasks
- `POST /api/tasks/bulk-delete/` - Bulk delete tasks
- `POST /api/tasks/bulk-complete/` - Bulk mark complete

#### Notifications
- `GET /api/notifications/` - List notifications
- `POST /api/notifications/send/` - Send notification
- `GET /api/notifications/history/` - Notification history

#### Analytics
- `GET /api/analytics/stats/` - Task statistics
- `GET /api/analytics/history/` - Task completion history
- `GET /api/analytics/user-tasks/` - All user tasks (admin)

---

## 🔔 Notification System

### 1. Email Notifications
- **Service**: SMTP (Gmail, SendGrid, etc.)
- **Use Cases**:
  - Task reminders
  - Daily/Weekly summaries
  - Overdue task alerts
- **Implementation**: Celery async tasks

### 2. WhatsApp Notifications
- **Service**: Twilio WhatsApp Business API
- **Use Cases**:
  - Important task reminders
  - Urgent notifications
- **Implementation**: Celery async tasks + Twilio SDK

### 3. Push Notifications
- **Service**: Firebase Cloud Messaging
- **Use Cases**:
  - Real-time task updates
  - Reminder alerts
  - App badges
- **Implementation**: Firebase Admin SDK + FCM tokens

### Notification Flow
```
1. User creates task with reminder
2. Backend stores task + schedules notification
3. Celery Beat triggers notification at scheduled time
4. Notification service sends via selected channel(s)
5. Status tracked in Notification model
```

---

## 🔄 Data Flow

### Task Creation Flow
```
1. User creates task in Flutter app
2. App saves to local Hive DB (offline support)
3. App sends POST request to Django API
4. Django validates and saves to PostgreSQL
5. Django schedules notification (if reminder set)
6. Django returns task with server ID
7. Flutter updates local DB with server ID
8. UI updates with new task
```

### Sync Flow
```
1. App comes online
2. Sync service compares local vs server timestamps
3. Upload local changes to server
4. Download server changes
5. Resolve conflicts (server wins or last-write-wins)
6. Update local DB
7. Refresh UI
```

---

## 🚀 Deployment Strategy

### Flutter App
- **Platform**: iOS App Store + Google Play Store
- **Build**: GitHub Actions CI/CD
- **Analytics**: Firebase Analytics

### Django Backend
- **Hosting Options**:
  - Railway / Render (easy deployment)
  - AWS EC2 + RDS (scalable)
  - DigitalOcean Droplet
  - Heroku
- **Database**: PostgreSQL (managed)
- **Redis**: Redis Cloud / AWS ElastiCache
- **Static Files**: AWS S3 or Cloudinary
- **Web Server**: Gunicorn + Nginx

---

## 🔐 Security Considerations

1. **Authentication**: JWT with refresh tokens
2. **HTTPS**: All API communication encrypted
3. **API Rate Limiting**: DRF throttling
4. **Input Validation**: Serializer validation
5. **SQL Injection**: ORM usage prevents
6. **XSS**: Sanitize user inputs
7. **CORS**: Configured for Flutter app only
8. **Environment Variables**: Secrets in .env files

---

## 📊 Future Enhancements

1. **Collaboration**: Share tasks with other users
2. **Attachments**: Add files to tasks
3. **Voice Input**: Create tasks via voice
4. **AI Suggestions**: Smart task categorization
5. **Recurring Tasks**: Daily/weekly repeating tasks
6. **Time Tracking**: Track time spent on tasks
7. **Integrations**: Google Calendar, Slack, etc.

---

## 🛠️ Development Setup

### Flutter App
```bash
flutter pub get
flutter run
```

### Django Backend
```bash
cd todo_backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Celery Worker
```bash
celery -A config worker -l info
celery -A config beat -l info
```

---

## 📝 API Documentation
- **Swagger UI**: `/api/docs/`
- **ReDoc**: `/api/redoc/`

---

**Version**: 2.0.0
**Last Updated**: 2025-11-08
