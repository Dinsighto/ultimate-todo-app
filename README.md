# Todo App 2025

A full-featured, multi-user todo application built with a clean, modern vibe-coding approach — minimal dependencies, maximum functionality.

**Live Demo** → https://todo-app-2tlb.onrender.com (your deployed version will have its own unique URL)

### Features

- Secure multi-user authentication (login/register with bcrypt hashing)
- Complete todo management: create, complete, delete, search
- Due dates with intelligent visual indicators (overdue, due today, upcoming)
- Tag system with customizable colors and multi-select support
- Full calendar view powered by FullCalendar.js
- Responsive dark mode with persistent user preference
- Automated email reminders 24 hours before due date (Resend integration)
- Progressive Web App (PWA) — fully installable on mobile and desktop
- Deployed entirely on Render's free tier with zero ongoing cost

### One-Click Deployment (Free Forever)

1. Fork or use this repository as a template
2. Sign in to [Render Dashboard](https://dashboard.render.com)
3. Create a new **Web Service** → connect your repository → select **Free** plan
4. Create a new **PostgreSQL** instance (Free tier) → copy the **Internal Database URL**
5. In your Web Service → **Environment** → add the following variables:

| Key              | Value Description                                            |
|------------------|--------------------------------------------------------------|
| `DATABASE_URL`   | Paste the Internal Database URL from your PostgreSQL instance |
| `SECRET_KEY`     | Any strong random string (e.g., `my-secret-2025-prod-key`)   |
| `RESEND_API_KEY` | Free API key from [resend.com](https://resend.com)           |
| `APP_URL`        | Your Render service URL (e.g., `https://todo-app.onrender.com`) |

6. (Recommended) Create a **Background Worker** → Command: `python scheduler.py` → add the same environment variables for email reminders

### Project Structure

```text
todo-app/
├── app.py              → Core Flask application and routing
├── models.py           → SQLAlchemy models (User, Todo, Tag)
├── scheduler.py        → Background job for daily email reminders
├── requirements.txt    → Exact dependency versions
├── render.yaml         → Render service configuration
├── Procfile            → Compatibility start command
├── runtime.txt         → Python version specification
├── static/
│   ├── style.css       → Modern responsive design with dark mode
│   ├── script.js       → Client-side interactions and PWA support
│   └── manifest.json   → Progressive Web App manifest
├── templates/
│   ├── base.html       → Layout template with navigation
│   ├── index.html      → Main todo list interface
│   ├── calendar.html   → FullCalendar integration
│   ├── login.html      → Login form
│   └── register.html   → Registration form
└── utils/
    └── email.py        → Resend email integration module
```

### Technology Stack
Flask 3.x
Flask-Login & Flask-SQLAlchemy
PostgreSQL (Render free tier)
Gunicorn web server
Resend (free email delivery)
FullCalendar.js
Vanilla JavaScript & CSS (no heavy frameworks)

### Credits
Professionally crafted in December 2025 through a collaborative vibe-coding session between Abdelrhman Mohamdeen and Grok (xAI).
Inspired by the pursuit of powerful, accessible tools without subscription barriers.
