release: 'cd ./okthen/okthen/ && python manage.py migrate'
web: sh -c 'cd ./okthen/ && exec gunicorn okthen.wsgi --log-file -'
