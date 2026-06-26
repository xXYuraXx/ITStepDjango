# Testy - testing platform

It's place where you can create your own test

Or discover tests created by other users

## Quickstart

In project folder run

```cmd
python manage.py runserver
```

## Docker

You can also check [Docker image](https://hub.docker.com/r/piprock/testy-django-app)

### Download

```cmd
docker pull piprock/testy-django-app:latest
```

### Run
```cmd
docker run -d -p 8000:8000 piprock/testy-django-app:latest
```
### Or docker compose
```cmd
docker compose up -d
```

Go to http://localhost:8000/

### Addition arguments

```Dockerfile
# docker run -e ...
# Port
APP_PORT=8000


# docker build --build-arg ...
# Project folder
BUILD_APP_PATH=/app
# Linux user
BUILD_USER_NAME=django_user
```

