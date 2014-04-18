update:
	pip install -r requirements.txt

run:
	foreman start -p 8080

develop:
	python manage.py runserver 8080
