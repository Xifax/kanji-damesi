# Core tasks
update:
	pip install -r requirements.txt

live:
	python manage.py gruntserver 8080

migrate:
	python manage.py syncdb
	python manage.py migrate saiban

# Misc tasks
run:
	foreman start -p 8080

develop:
	python manage.py runserver 8080

