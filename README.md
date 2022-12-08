# Проект ride_recording
[![ride_workflow](https://github.com/niktere12321/ride_recording/actions/workflows/ride_workflow.yml/badge.svg)](https://github.com/niktere12321/ride_recording/actions/workflows/ride_workflow.yml)

## Описание

Ride_recording это сервис для аренды транспортных средств(квадроцикл, катер и т.п.) только для сотрудников компании.

Пользователи могут:
- забронировать в определеный день одно из перечисленых транспортных средств;
- удалять свою запись;
- просмотривать историю своих поездок;
- смотреть все свои будующие записи.

Администраторы могут:
- отправлять приглашение на почту для новых пользователей;
- редактировать информацию аккаунтов пользователей;
- удалять пользователей;
- удалять записи всех пользователей;
- добавлять и удалять транспортные средства;
- смотреть статистику.

## Технологии
- Python 3.7.9
- Django 2.2.28

## Установка проекта локально

* Склонировать репозиторий на локальную машину:
```bash
git clone https://github.com/niktere12321/ride_recording.git
```
```bash
cd ride_recording
```

- Создать и заполнить по образцу .env-файл
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
EMAIL_HOST_USER=<...>
EMAIL_HOST_PASSWORD=<...>
secret_key=<...>
```

* Cоздать и активировать виртуальное окружение:

```bash
python -m venv venv
```

```bash
source venv/Scripts/activate
```

* Установить зависимости из файла requirements.txt:

```bash
python3 -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

* Выполните миграции:
```bash
cd ride
```
```bash
python manage.py migrate
```

* Запустите сервер:
```bash
python manage.py runserver
```

## Запуск проекта в Docker контейнере
* Установите Docker.

Параметры запуска описаны в файлах `docker-compose.yml` и `nginx.conf` которые находятся в директории `infra/`.  
При необходимости добавьте/измените адреса проекта в файле `nginx.conf`

* Запустите docker compose:
```bash
docker-compose up -d --build
```  
  > После сборки появляются 3 контейнера:
  > 1. контейнер базы данных **db**
  > 2. контейнер бекэнда **web**
  > 3. контейнер web-сервера **nginx**
* Примените миграции:
```bash
sudo docker compose exec web python manage.py makemigrations users
sudo docker compose exec web python manage.py migrate users
sudo docker compose exec web python manage.py makemigrations records
sudo docker compose exec web python manage.py migrate records
sudo docker compose exec web python manage.py migrate
```
* Создайте администратора:
```bash
sudo docker compose exec web python manage.py createsuperuser
```
* Соберите статику:
```bash
sudo docker compose exec web python manage.py collectstatic --noinput
```

---
## Техническая информация

Стек технологий: Python 3, Django, Django Rest, Docker, PostgreSQL, nginx, gunicorn, Djoser.

Веб-сервер: nginx (контейнер nginx)
Backend фреймворк: Django (контейнер web)  
API фреймворк: Django REST (контейнер web)  
База данных: PostgreSQL (контейнер db)

Веб-сервер nginx перенаправляет запросы клиентов к контейнеру web, либо к хранилищам (volume) статики и файлов.  
Контейнер nginx взаимодействует с контейнером web через gunicorn.  

---
## Об авторе

Терехов Никита Алексеевич
