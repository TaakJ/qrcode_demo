release: python manage.py migrate
web: daphne qrcode_demo.asgi:application --port $PORT --bind 0.0.0.0 -v2
celery: celery -A qrcode_demo.celery worker -l info
celerybeat: celery -A qrcode_demo beat -l INFO 
celeryworker2: celery -A qrcode_demo.celery worker & celery -A qrcode_demo beat -l INFO & wait -n