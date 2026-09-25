# BookMySeat

A simple Django movie-ticket booking website for browsing movies, choosing a theatre and showtime, selecting seats, and viewing booking history.

## Features

- Movie listing and details
- Theatre and showtime selection
- Visual seat selection with duplicate-seat protection
- Registration, login, logout, profile, and booking history
- Django admin for movies, theatres, shows, seats, and bookings
- SQLite locally and PostgreSQL on Render

## Local setup

```bash
python -m venv venv
# Windows: venv\\Scripts\\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/`, then add movies, theatres, and future shows at `/admin/`.

## Render deployment

Create a PostgreSQL database and a Python web service connected to this repository. Use `pip install -r requirements.txt` as the build command, or use `bash build.sh`. Use `gunicorn Bookmyseat.wsgi:application` as the start command.

Set these environment variables in Render:

- `SECRET_KEY`: a long random secret
- `DEBUG`: `False`
- `DATABASE_URL`: the Render PostgreSQL connection string
- `ALLOWED_HOSTS`: your Render hostname
- `CSRF_TRUSTED_ORIGINS`: `https://your-render-hostname`

Movie poster uploads use local media storage for this simple project. Render's local filesystem is ephemeral, so use poster files that can be re-uploaded or add persistent storage before treating this as a production service.
