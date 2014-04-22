# Core tasks
update:
	pip install -r requirements.txt && \
		cd client && npm install && bower update

live:
	python manage.py gruntserver 8080

migrate:
	python manage.py syncdb
	python manage.py migrate

# Misc tasks
run:
	foreman start -p 8080

develop:
	python manage.py runserver 8080

new-migration:
	python manage.py sql saiban && \
		python manage.py schemamigration saiban --auto


