Kanji Damesi
------------

# What is it

Rite-of-passage Django app inspired by Anki, Readthekanji, and Kanjibox.
Much SRS, very radical decomposition, so python.

# Setting up new repo

Create new virtual env, source it and run `make`. Otherwise, perform the
following ritual:

1. Initialize new virtual environment & install python modules

        virtualenv venv; source venv/bin/activate; make

2. Initialize node modules, install bower components and build frontend app

        cd client; npm install; bower install; grunt build

3. Collect static files and sync database

        cd -; ./manage.py collectstatic; make migrate

4. Launch Django server with grunt live reload

        make live; open http://localhost:8080

# Why

For fun and profit.
Also to consolidate various japanese resources for better 'guess correct kanji
from group until you are bored out of your mind experience'.
