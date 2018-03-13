release: 'python /app/okthen/manage.py migrate'
web: sh -c 'cd ./okthen/ && exec gunicorn okthen.wsgi --log-file -'
