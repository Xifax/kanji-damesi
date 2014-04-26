# Core tasks
update:
	pip install -r requirements/dev.txt && \
		cd client && npm install && bower update

release:
	pip install -r requirements/master.txt
	cd client && npm install && bower update && grunt build
	python manage.py collectstatic

live:
	python manage.py gruntserver 8080

migrate:
	python manage.py syncdb
	python manage.py migrate

# Misc tasks
test:
	python manage.py test saiban
	grunt --gruntfile=client/Gruntfile.coffee test

run:
	foreman start -p 8080

develop:
	python manage.py runserver 8080

new-migration:
	python manage.py sql saiban && \
		python manage.py schemamigration saiban --auto

docs:
	pycco saiban/*.py -d docs

