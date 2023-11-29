[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![Django-app workflow](https://github.com/makcfd/foodgram-project-react/actions/workflows/foodgram.yaml/badge.svg)](https://github.com/makcfd/foodgram-project-react/actions/workflows/foodgram.yaml)

# ПProject "Food Helper" - Foodgram

## Description
On this service, users can publish recipes, subscribe to the publications of other users, add their favorite recipes to the “Favorites” list, and before going to the store, download a consolidated list of products needed to prepare one or more selected dishes.

## Start the project

- Server login:
```
ssh <server user>@<server IP>
```

- Clone repo:
```
git clone git@github.com:makcfd/foodgram-project-react.git
```

- Install Docker on server:
```
sudo apt install docker.io
```
- Install Docker Compose (for Linux):
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
- Persmissions docker-compose:
```
sudo chmod +x /usr/local/bin/docker-compose
```
- Open infra folder:
```
cd foodgram-project-react/infra
```
- Create env-file:
```
touch .env
```
- Add info for DB:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
- Get docker images:
```
sudo docker pull makcfd/backend
sudo docker pull makcfd/frontend
```
- Launch:
```
sudo docker-compose up -d
```
- Initiate migrations in Django:
```
sudo docker-compose exec -T backend python manage.py makemigrations
sudo docker-compose exec -T backend python manage.py migrate
```
- Get static files:
```
sudo docker-compose exec -T backend python manage.py collectstatic --no-input
```
- Load initial data:
```
sudo docker compose cp /home/< your user name >/foodgram-project-react/data/dump.json backend:/app/dump.json
sudo docker compose exec backend python manage.py loaddata dump.json
```

## Runnig project example
- Url:
http://62.84.121.103/

- Credentials:
login: admin@admin.com
psw: admin
