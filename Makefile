update:
	pip install -r requirements.txt

run:
	foreman start -p 8080

develop:
	python manage.py runserver 8080

migrate:
	python manage.py syncdb
	python manage.py migrate saiban
