# foodgram-project
foodgram-project

## Installing

`./manage.py makemigrations`  
`./manage.py migrate`  

Импортируйте теги в базу - выполните команду `./manage.py load_tags`  

Чтобы импортировать ингридиенты из файла `ingredients.json` - выполните команду
`./manage.py import_ingredients_from_json_file`

Создайте администратора сайта `./manage.py createsuperuser`  

Чтобы запустить проект на локальной машине - `./manage.py runserver`