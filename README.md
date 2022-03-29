# Foodgram project

![Foodgram-project-react](https://github.com/squisheelive/foodgram-project-react/actions/workflows/main.yml/badge.svg)
#### Дипломный проект курса python-разработчик от Яндеск Практикум.
В этом проекте реализован API для небольшого сервиса по созданию и обмену рецептами. Бэкенд реализован на основе [Django REST framework](https://www.django-rest-framework.org/) под уже готовый [React](https://ru.reactjs.org/) фронтенд. Сервис развернут через контейнеризацию [Docker](https://www.docker.com/), на мощностях Yandex Cloud и доступен по адресу: http://51.250.8.175/
#### Для запуска проекта локально:

- Клонировать репозиторий и перейти директорию `/infra`.

- Создать там файл `.env` со следующим содержимым:

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=user
POSTGRES_PASSWORD=password
DB_HOST=db
DB_PORT=5432
```

- Следует придумать свои имя пользователя и пароль для базы данных и заменить соответствующие значения `POSTGRES_USER` и `POSTGRES_PASSWORD`.

- Запустить контейнеризацию docker `docker-compose up`

- Выполнить миграции и собрать статику:

```
docker-compose exec web python manage.py migrate
```
```
docker-compose exec web python manage.py collectstatic --no-input
```
- Загрузить тестовые данные:
```
docker-compose exec web python manage.py add_ingredients data/ingredients.csv
```
```
docker-compose exec web python manage.py loaddata db.json
```
- Документацию к API ищите [здесь](http://localhost/api/docs/redoc.html)
- Попасть в [админку](http://localhost/admin) можно с пользователем и паролем `admin`
