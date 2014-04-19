Kanji Damesi
------------

Scaffolding for Heroku application.
Django project with separate AngularJS frontend.

Setting up new repo:

1. Initialize new virtual environment & install python modules

    virtualenv venv; source venv/bin/activate; make

2. Initialize node modules, install bower components and build frontend app

    client; npm install; bower install; grunt build

3. Collect static files

    cd -; ./manage.py collectstatic

4. Launch Django server with grunt live reload

    make live
