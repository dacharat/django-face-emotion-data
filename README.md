# Web-face-recognition

## Setup
- run `docker-compose up -d` to start PostgreSQL database.
- run `docker exec -it my_postgres psql -U postgres` to open shell of PostgreSQL.

#### If you don't have Docker Compose
- Use `docker run -d -p 54320:5432 --volume ~/dev/py3_keras/django-face-emotion-data/data:/var/lib/postgresql/data --name my_postgres postgres:11` to create PostgreSQL container.


## In PostgreSQL shell
- `\l` to see list of database
- `\c my_face_data` to use database name `my_face_data`(databasee for this web)
- `\dt` to see list of table in this database
- `select face from test_person;` example of query command

## Django command
- `django-admin.py startproject mysite .` to create this project
- `python manage.py makemigrations` check diffent to database 
- `python manage.py migrate` migrate the change to database
- `python manage.py runserver 0.0.0.0:3000` run with port 3000
- `python manage.py shell` open django shell
- `python manage.py createsuperuser` create user for admin page
- `python manage.py startapp graph` create new model name `graph`
- `python manage.py inspectdb` see all table in database