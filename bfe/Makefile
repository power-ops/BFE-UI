.PHONY: initial

install:
	python manage.py makemigrations
	python manage.py migrate

admin:
	python manage.py createsuperuser

hans:
	django-admin makemessages -l zh_hans
	django-admin compilemessages

run:
	python manage.py runserver 0.0.0.0:8000