#!/bin/bash
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (cd hackingtools; python manage.py createsuperuser --no-input; cd ..)
fi
(cd hackingtools; gunicorn hackingtoolsgui.wsgi --user www-data --bind 0.0.0.0:8010 --workers 3) &
nginx -g "daemon off;"