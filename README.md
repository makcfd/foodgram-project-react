[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![Django-app workflow](https://github.com/makcfd/foodgram-project-react/actions/workflows/foodgram.yaml/badge.svg)](https://github.com/makcfd/foodgram-project-react/actions/workflows/foodgram.yaml)

# Проект "Продуктовый помощник" - Foodgram

## Описание
На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Подготовка и запуск проекта

- Зайти на сервер:
```
ssh <server user>@<server IP>
```

- Клонировать репозиторий:
```
git clone git@github.com:makcfd/foodgram-project-react.git
```

- Установить Docker на сервер:
```
sudo apt install docker.io
```
- Установить Docker Compose (for Linux):
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
- Выдать разрешения на команду docker-compose:
```
sudo chmod +x /usr/local/bin/docker-compose
```
- Перейти в папку infra клонированного репозитория:
```
cd foodgram-project-react/infra
```
- Созднать env-file:
```
touch .env
```
- В созданный файл добавить следующую информацию:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
- Скачиваем образы:
```
sudo docker pull makcfd/backend
sudo docker pull makcfd/frontend
```
- Запускаем:
```
sudo docker-compose up -d
```
- Делаем миграции:
```
sudo docker-compose exec -T backend python manage.py makemigrations
sudo docker-compose exec -T backend python manage.py migrate
```
- Собираем статику:
```
sudo docker-compose exec -T backend python manage.py collectstatic --no-input
```
- Загружаем данные, при необходимости:
```
sudo docker compose cp /home/< your user name >/foodgram-project-react/data/dump.json backend:/app/dump.json
sudo docker compose exec backend python manage.py loaddata dump.json
```

## Пример проекта развернутого на сервере
- Url:
http://158.160.72.24/

- Credentials:
login: admin@admin.com
psw: admin
