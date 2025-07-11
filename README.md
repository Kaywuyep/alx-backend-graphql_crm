# GRAPHQL-DJANGO

**commands**
```bash
django-admin startproject alx_backend_graphql_crm
cd alx_backend_graphql_crm
python manage.py startapp crm
# install required dependencies, do this in a virtual environment
pip install graphene-django django-filter

# migrate
python manage.py runserver
python manage.py makemigrations	# Creates new migration files based on model changes
python manage.py migrate	# Applies those migrations to the database
python manage.py showmigrations	# Lists migrations and their applied status
python manage.py sqlmigrate <app_name> <migration_number>
```

**Note create a virtual environment**
```bash
python -m venv venv
pip install -r requirement.txt
pip freeze > requirement.txt  #  to add new dependencies to the requirement.txt file
```

<!-- Register the Cron Jobs -->
```bash
python manage.py crontab add
python manage.py crontab show
```

