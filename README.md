# YaMDb API
ридми еще в процессе

### Технологии
- Python 3.7+
- [django](https://github.com/django/django) 2.2.16
- [django-rest-framework](https://github.com/encode/django-rest-framework) 3.12.4
- [Simple JWT](https://github.com/jazzband/djangorestframework-simplejwt) 5.2.0

### Запуск проекта в dev-режиме
Клонировать репозиторий
Установить и активировать виртуальное окружение
```
$ python3 -m venv venv

# Активация окружения для Mac или Linux:
$ source venv/bin/activate 
# и для Windows:
$ source venv/Scripts/activate 
``` 
Установить зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 
Выполнить миграции и запустить проект
```
python3 manage.py migrate
python3 manage.py runserver
``` 
### Получение персонального токена
Для взаимодействия с API необходимо завести учетную запись пользователя, 
или суперпользователя и иметь персональный токен, для чего необходимо 
перейти по адресу .../api/v1/auth/signup/ и отправить POST запрос с 
именем и адресом электронной почты пользователя
```
{
    "username": "example_name",
    "email": "example_email"
}
``` 
Получить токен (в ключе access) и передать его в headers
```
KEY: Authorization
VALUE: Bearer <ваш токен>
``` 
### Примеры запросов
**Полный список запросов можно посмотреть перейдя на .../redoc/ 
развернутого проекта**
### Наша команда
Александр Усольцев, Максим Захаров, Алексей Вьюник