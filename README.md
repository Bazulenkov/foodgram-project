![workflow foodgram](https://github.com/Bazulenkov/foodgram-project/workflows/foodgram%20CI%2fCD/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
# foodgram-project
Приложение «Продуктовый помощник»: сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд. 

На момент создания этого файла ресурс доступен по адресу: http://food-gram.cf (Но это не навсегда :) 
## Installing

`./manage.py migrate`  

Импортируйте теги в базу - выполните команду `./manage.py load_tags`  

Чтобы импортировать ингридиенты из файла `ingredients.json` - выполните команду
`./manage.py import_ingredients_from_json_file`

Создайте администратора сайта `./manage.py createsuperuser`  

Чтобы запустить проект на локальной машине - `./manage.py runserver`

## Built With
- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Django REST framework](https://www.django-rest-framework.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)
- [Gunicorn](https://gunicorn.org/)
- [NGINX](https://nginx.org)

## Authors

* **Anton Bazulenkov** - *Initial work* - [Bazulenkov](https://github.com/Bazulenkov)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
