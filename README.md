### tma-v2-23f3001065

# Trekking Management Application (TMA)

A full-stack web application developed as part of the Modern Application Development II project.

The application allows trekkers to browse and book treks, staff members to manage assigned treks, and administrators to manage the overall trekking system through role-based access control.

---

## Features

### Authentication & Authorization
- User Registration
- User Login
- Staff Login
- Admin Login
- JWT-based Authentication
- Role-Based Access Control

### Admin Module
- Dashboard Statistics
- Create, Edit and Delete Treks
- Create Staff Accounts
- Assign Staff to Treks
- View Users
- Activate / Deactivate Users
- View All Bookings

### Staff Module
- View Assigned Treks
- Update Trek Status and Available Slots
- View Trek Details
- View Registered Participants

### Trekker Module
- Browse Available Treks
- Search Treks
- View Trek Details
- Book Treks
- Cancel Bookings
- Re-book Cancelled Treks
- Export Booking History

### Background Jobs
- Email Booking History as CSV
- Daily Trek Reminder Emails
- Monthly Admin Report
- Celery + Redis Integration

### Performance Optimization
- Redis Caching for Frequently Accessed Data

---

## Technology Stack

### Backend
- Flask
- Flask-RESTful
- SQLAlchemy
- Flask-JWT-Extended
- Flask-Mail
- Flask-Caching
- Celery
- Redis
- SQLite

### Frontend
- Vue 3
- Vue Router
- Axios
- Bootstrap

---

## Project Structure

```text
backend/
├── models/
├── routes/
├── database/
├── app.py
├── app_factory.py
├── celery_app.py
└── tasks.py

frontend/
├── src/views/
├── src/router/
├── App.vue
└── main.js
```

---

## Database Design

Main Entities:

- Users
- Staff Profiles
- Treks
- Bookings

Relationships:

- One User can have many Bookings
- One Trek can have many Bookings
- One Staff User has one Staff Profile
- One Staff Profile can manage multiple Treks

---

## Setup

### Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Frontend Dependencies

```bash
cd frontend
npm install
```

### Redis

Start Redis:

```bash
sudo systemctl start redis
```

Check Redis:

```bash
redis-cli ping
```

Expected output:

```text
PONG
```

---

## Running the Application

### 1. Start Backend

```bash
cd backend
python3 app.py
```

Backend runs on:

```text
http://127.0.0.1:5000
```

### 2. Start Frontend

```bash
cd frontend
npm run dev
```

Frontend runs on:

```text
http://localhost:5173
```

### 3. Start Celery Worker

```bash
cd backend
celery -A celery_app.celery worker --loglevel=info
```

### 4. Start Celery Beat

```bash
cd backend
celery -A celery_app.celery beat --loglevel=info
```

---

## Test Email Service

Open:

```text
http://127.0.0.1:5000/send-test-email
```

If configured correctly, a test email will be queued and sent using Celery.

---

## Author

Bhavana Gupta  
Roll Number: 23f3001065