# YaMDb API

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles).
Произведения делятся на категории: "Книги", "Фильмы", "Музыка". Список
категорий (Category) может быть расширен администратором.

В каждой категории есть произведения: книги, фильмы или музыка. 

Произведению может быть присвоен жанр (Genre) из списка предустановленных (
например, "Сказка", "Рок" или "Артхаус"). Новые жанры может создавать только
администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые
отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти (
целое число); из пользовательских оценок формируется усреднённая оценка
произведения — рейтинг (целое число). На одно произведение пользователь может
оставить только один отзыв.

## Технологии

- Python 3.7+
- [django](https://github.com/django/django) 2.2.16
- [django-rest-framework](https://github.com/encode/django-rest-framework)
  3.12.4
- [Simple JWT](https://github.com/jazzband/djangorestframework-simplejwt) 5.2.0

## Запуск проекта в dev-режиме

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

## Получение персонального токена

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

После успешной регистрации на указаный email придет секретный код, который
необходимо скопировать в поле "confirmation_code" по адресу ...
/api/v1/auth/token/ и получить персональный токен

```
{
    "username": "example_name",
    "confirmation_code": "your_code"
}
``` 

Далее передаем полученный токен в headers

```
KEY: Authorization
VALUE: Bearer <ваш токен>
``` 

## Примеры запросов

**Полный список запросов можно посмотреть перейдя на .../redoc/
развернутого проекта**
