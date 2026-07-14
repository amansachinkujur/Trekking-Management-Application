# Trekking Management Application

A full-stack web application developed for the **Modern Application Development II (MAD2)** course at **IIT Madras**. The application enables Admins, Trek Staff, and Users to manage trekking activities through role-based access, online bookings, background jobs, email notifications, and Redis caching.

---

# Features

## Authentication
- JWT-based authentication
- Role-based access control (Admin, Staff, User)
- User registration and login
- Admin and Staff login

## Admin
- Create, update and delete treks
- Add and manage trek staff
- Assign staff to treks
- Manage users and bookings
- Search users, staff and treks
- Activate/Deactivate users
- Dashboard with trekking statistics

## Trek Staff
- View assigned treks
- Update trek status
- Update available slots
- View registered participants
- Mark treks as completed

## User
- Register and login
- Browse available treks
- Search and filter treks
- Book and cancel treks
- View trekking history
- Export booking history as CSV

---

# Background Jobs (Celery)

### Daily Reminder
Sends reminder emails to users one day before their trek starts.

### Monthly Activity Report
Generates an HTML report containing trekking statistics and emails it to the Admin.

### CSV Export
Users can export their booking history as a CSV file, which is generated asynchronously and emailed to them.

---

# Redis Caching

- Frequently accessed trek listings are cached.
- Cache expiry is set to **5 minutes**.
- Cache is automatically cleared whenever trek information is modified.

---

# Technology Stack

### Frontend
- Vue.js
- Vue Router
- Bootstrap
- Vite

### Backend
- Flask
- SQLAlchemy
- Flask-JWT-Extended
- Flask-Mail

### Database
- SQLite

### Background Processing
- Celery
- Redis-compatible server (Memurai)

---

# Project Structure

```
Trekking-Management-Application
│
├── backend
│   ├── app
│   ├── celery_worker.py
│   ├── config.py
│   ├── run.py
│   └── requirements.txt
│
├── frontend
│   ├── public
│   ├── src
│   │   ├── assets
│   │   ├── components
│   │   ├── router
│   │   ├── stores
│   │   └── views
│   └── package.json
│
└── README.md
```

---

# Installation

## Terminal 1 - Backend

```bash
cd backend

python -m venv .venv
```

Activate virtual environment

### Windows (PowerShell)

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies

```bash
pip install -r requirements.txt
```

Set mail environment variables

```powershell
$env:MAIL_USERNAME=""
$env:MAIL_PASSWORD=""
```

Run Flask

```bash
python run.py
```

---

## Terminal 2 - Frontend

```bash
cd frontend

npm install
```

Run Vue

```bash
npm run dev
```

---

## Terminal 3 - Celery Worker

```bash
cd backend
```

Activate virtual environment

```powershell
.venv\Scripts\Activate.ps1
```

Set environment variables again (Celery runs in a separate process)

```powershell
$env:MAIL_USERNAME=""
$env:MAIL_PASSWORD=""
```

Start Celery

```bash
python -m celery -A celery_worker:celery worker --pool=solo --loglevel=info
```

---

# Memurai (Redis)

This project was developed on Windows using **Memurai**, a Redis-compatible server.

Before starting the Celery worker, ensure Memurai is running.

Check its status

```powershell
Get-Service Memurai
```

Expected output

```
Status   Name
------   ----
Running  Memurai
```

If it is stopped, open **PowerShell as Administrator** and start it using

```powershell
Start-Service Memurai
```

or

```powershell
net start Memurai
```


---

# Environment Variables

Only the following variables need to be configured:

```text
MAIL_USERNAME
MAIL_PASSWORD
MAIL_DEFAULT_SENDER
```

---

# Celery Command Explained

```bash
python -m celery -A celery_worker:celery worker --pool=solo --loglevel=info
```

| Command | Description |
|----------|-------------|
| `python -m celery` | Starts the Celery module |
| `-A celery_worker:celery` | Loads the Celery application named `celery` from `celery_worker.py` |
| `worker` | Starts the Celery worker process |
| `--pool=solo` | Uses a single worker process (recommended on Windows) |
| `--loglevel=info` | Displays task execution logs |

---

# Project Workflow

```
Browser

↓

Vue Frontend

↓

Flask API

↓

SQLite Database

↓

Redis (Memurai)

↓

Celery Worker

↓

Email / CSV Export
```

---

# Core Functionalities

- Prevent duplicate bookings
- Prevent overbooking
- Booking allowed only for Open treks
- Staff can manage only assigned treks
- Trekking history for every user
- Search and filter treks
- Admin dashboard with statistics

---

# Future Improvements

- Payment gateway integration
- PDF reports
- Interactive analytics dashboard
- Push notifications
- Cloud deployment

---

# Author

**Aman Sachin Kujur**