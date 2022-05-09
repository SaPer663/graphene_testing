# Платформа для блогеров
### Описание
Yatube - это социальная сеть. Она даёт пользователям возможность создать учетную запись, публиковать записи, подписываться на любимых авторов и отмечать понравившиеся записи. 
### Технологии
- [Python 3.8](https://www.python.org/)
- [`Django 2.2.28`](https://github.com/django/django)
- [`graphene-django 2.15.0`](https://github.com/graphql-python/graphene) для API
- [`poetry 1.1.7`](https://github.com/python-poetry/poetry) для управления зависимостями
- [`pytest `](https://pytest.org/)  для юнит тестов
- [`flake8 4.0.1`](http://flake8.pycqa.org/en/latest/) линтер
- [`docker`](https://github.com/docker) для развёртывания
### Запуск проекта в dev-режиме
Для запуска проекта необходимо в директории ```yatube/config``` создать ```.env.dev``` на основе ```.env.template```.
- склонируйте репозиторий
```
git clone https://github.com/SaPer663/yatube.git
```
- соберите образ контейнера
```
docker-compose build
```
- запустите контейнер
```
docker-compose up
```
- после запуска контейнера сервер будет доступен по адресу:
```
http://0.0.0.0:8000/
```
- документация API доступна по адресу:
```
http://0.0.0.0:8000/swagger/
```

### Авторы
Александр @saper663 
