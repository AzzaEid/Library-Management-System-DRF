runserver:
	python LMS/manage.py runserver

run:
	DJANGO_ENV=development python LMS/manage.py runserver

migrate:
	python LMS/manage.py migrate

migrations:
	python LMS/manage.py makemigrations

createsuperuser:
	python LMS/manage.py createsuperuser

freeze:
	pip freeze > requirements.txt