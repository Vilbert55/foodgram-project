![foodgram](https://github.com/Vilbert55/foodgram-project/workflows/foodgram/badge.svg)
# foodgram-project

Демо: [http://quickcookies.cf/](http://quickcookies.cf// "Продуктовый помощник")

## Описание

Онлайн-сервис в котором пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», добавлять рецепты в список покупок, фильтровать рецепты по тегам, выгружать в txt-файл список всех нужных ингредиентов для рецептов из списка покупок.

## Установка и запуск

Для работы требуется **Docker** и **Docker-compose**

Сохраните файлы **docker-compose.yaml** и **nginx.conf**

В этой же диретории создайте файл .env со следующим содержимым
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=(придумайте свой)
DB_HOST=db
DB_PORT=5432
SECRET_KEY= (придумайте свой)
NGINX_HOST=127.0.0.1 
NGINX_PORT=80  
```
Замените значения *server_name* в файле **nginx.conf** на *127.0.0.1 localhost*

Спульте образы и запустите контейнеры командой
```
docker-compose up -d
```
Зайдите в контейнер приложения
```
docker exec -it foodgram-project_web_1 bash
```
Можно загрузить ингредиенты в базу из готового списка ingredients.json (находится рядом с manage.py) командой
```
python manage.py loadingredients
```
Создайте суперпользователя
```
python manage.py createsuperuser
```

Приложение доступно по адресу *localhost:80*