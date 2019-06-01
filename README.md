# Captstone project server

## start er up

This server is based on the django example app tutorial available at <>.
django apps are managed from the project root directory, you need to use the linux shell.

```
# init the database
python3 manage.py makemigrations jsonapi
python3 manage.py migrate

# create an admin account
python3 manage.py createsuperuser

```

access the admin interface at <http://127.0.0.1:8000/admin/>

## ./ProjectServer

this directory contains the project configuration.
server admin should only have to muck around in here.

## ./jsonapi

this directory contains the json api, this is also where the database and models are.

## ./frontend

this directory contains a frontend app.
it sucks.
we don't actually need it for the demonstration so it may not be finished by then.
