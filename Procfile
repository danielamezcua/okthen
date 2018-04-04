release: cd ./okthen/ && python manage.py makemigrations && python manage.py migrate
web: sh -c 'cd ./okthen/ && exec gunicorn okthen.wsgi --log-file -'
