# API на GraphQl
### Описание
Это API на GraphQL сделано для ознакомления с протоколом GraphQL и в частности 
с библиотекой    ```graphene-django```

Через API можно получить информацию о фильмах(состав актёров, год выхода на экраны, название) и об актёрах(имя_фамилию), которые в них снимались.
### Технологии
- [`Python 3.8`](https://www.python.org/)
- [`Django 2.2.28`](https://github.com/django/django) для моделей
- [`graphene-django 2.15.0`](https://github.com/graphql-python/graphene) для API
- [`poetry 1.1.7`](https://github.com/python-poetry/poetry) для управления зависимостями
- [`flake8 4.0.1`](http://flake8.pycqa.org/en/latest/) линтер
- [`docker 20.10.14`](https://github.com/docker) для развёртывания
### Запуск проекта в dev-режиме

- склонируйте репозиторий
```
git clone https://github.com/SaPer663/graphene_testing.git
```
- в директории ```api_on_graphql/config``` необходимо создать ```.env``` файл на основе ```.env.template```.

- соберите образ контейнера
```
docker build . -t graph_image
```
- сделайте миграции в базе данных
```
docker run -v $(pwd)/api_on_graphql:/code -p 8000:8000 -w /code/ graph_image python manage.py migrate
```
- заполните базу данными из файла movies.json
```
docker run -v $(pwd)/api_on_graphql:/code -p 8000:8000 -w /code/ graph_immage \
python manage.py loaddata movies.json
```
- запустите контейнер
```
docker run -v $(pwd)/api_on_graphql:/code -p 8000:8000 -w /code/ graph_image \
python manage.py runserver 0.0.0.0:8000
```
- после запуска контейнера сервер будет доступен по адресу:
```
http://0.0.0.0:8000/
```
По адресу ```http://127.0.0.1:8000/graphql/``` можно тестировать API через
[`GraphiQL`](https://www.electronjs.org/apps/graphiql) — встроенной IDE для выполнения запросов.

### Примеры запросов
Получить имя и id всех актёров
```
query getActors {  
  actors {
    id
    name
  }
}
```
или
```
curl -g \
-X POST \
-H "Content-Type: application/json" \
-d '{"query":"query getActors {actors {id name}}"}' \
http://0.0.0.0:8000/graphql/
```
Ответ от сервера:
```
{
  "data": {
    "actors": [
      {
        "id": "6",
        "name": "Александр Демьяненко"
      },
      {
        "id": "5",
        "name": "Владимир Этуш"
      },
      {
        "id": "2",
        "name": "Георгий Вицин"
      },
      {
        "id": "3",
        "name": "Евгений Моргунов"
      },
      {
        "id": "4",
        "name": "Леонид Куравлёв"
      },
      {
        "id": "7",
        "name": "Наталья Крачковская"
      },
      {
        "id": "8",
        "name": "Наталья Селезнёва"
      },
      {
        "id": "1",
        "name": "Юрий Никулин"
      }
    ]
  }
}
```
Получить данные и фильме по id
```
query getMovie {  
  movie(id: 1) {
    id
    title
    actors {
      id
      name
    }
  }
}
```
или
```
curl -g \
-X POST \
-H "Content-Type: application/json" \
-d '{"query":"query getMovie { movie(id: 1){id title actors{id name}}}"}' \
http://0.0.0.0:8000/graphql/
```
Ответ:
```
{
  "data": {
    "movie": {
      "id": "1",
      "title": "Самогонщики",
      "actors": [
        {
          "id": "2",
          "name": "Георгий Вицин"
        },
        {
          "id": "3",
          "name": "Евгений Моргунов"
        },
        {
          "id": "1",
          "name": "Юрий Никулин"
        }
      ]
    }
  }
}
``` 

### Авторы
Александр @saper663 
