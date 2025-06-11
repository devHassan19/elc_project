# ELC Project

A Django-based web application designed for managing and serving dynamic content. This project uses the Django framework and includes user interfaces, routing, models, forms, and template rendering.

## 🚀 Features

- Django web framework setup  
- SQLite3 database integration  
- Structured templates and static files  
- Forms and models integration  
- Admin panel enabled  
- Scalable project structure with `main_app` as the core app  

## 🧱 Project Structure

```
elc_project-main/
├── elc/              # Django project settings (settings, urls, wsgi, asgi)
├── main_app/         # Core Django app (views, models, forms, templates)
├── staticfiles/      # Collected static files (CSS, JS, images)
├── db.sqlite3        # SQLite database
├── manage.py         # Django management script
├── requirements.txt  # Python dependencies
├── Pipfile           # Pipenv environment configuration
├── build.sh / start.sh # Shell scripts for deployment or startup
```

## 📦 Requirements

- Python 3.8+
- Django (as defined in `requirements.txt` or `Pipfile`)
- pip or pipenv

## ⚙️ Installation

### Using pip:
```bash
git clone https://github.com/devHassan19/elc_project.git
cd elc_project
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Using pipenv:
```bash
pipenv install
pipenv shell
python manage.py migrate
python manage.py runserver
```

## 🖥️ Usage

After starting the server, access the application at:
```
http://127.0.0.1:8000/
```

### Admin Panel
To create a superuser and access the admin panel:
```bash
python manage.py createsuperuser
```
Then open:
```
http://127.0.0.1:8000/admin/
```

## 📄 License

This project is open source. You can include the MIT license or any other license if publishing publicly.

```
MIT License
```

---

## ✍️ Author

Developed by [@devHassan19](https://github.com/devHassan19)
