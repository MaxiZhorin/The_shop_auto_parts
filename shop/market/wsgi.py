# -*- coding: utf-8 -*-

import os,sys

#путь к проекту
sys.path.insert(0, '/home/g/ganse0yand/site1/public_html/')
#путь к фреймворку
sys.path.insert(0, '/home/g/ganse0yand/site1')
#путь к виртуальному окружению
sys.path.insert(0, '/home/g/ganse0yand/site1/public_html/market/myvenv/lib/python3.4/site-packages')
os.environ["DJANGO_SETTINGS_MODULE"] = "market.settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()