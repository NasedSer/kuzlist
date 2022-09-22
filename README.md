# Перечень Кузбасс
# Выгрузка приложения на хостинг

1. Требования к размещению
2. Наличие установленного python3.10 и выше
1. Желательно наличие `bash console` или `менеджера файлов`
1. Если это нет, то 
2. Создать `вертуальное окружение`
    1. клонировать проект с https://github.com/NasedSer/kuzlist/ 
    1.
    ```sh
        python3 -m venv env
    ```

1. Активировать `venv` and install all dependencies (из файла requirements.txt)
1. Создать `new custom webapp` 
1. Fill in all the gaps
    1. Source code: - the path to the folder with `manage.py` (/home/denniskot/django-dummy/src)
    1. Virtualenv:
        1. The path to the folder with virtual env (`/home/denniskot/django-dummy/env`)
    1. Static files:
        1. Create in bash conslole folders `static` and `media` on the same level as `src` folder. (/home/denniskot/django-dummy/static and /home/denniskot/django-dummy/media)
        1. Add url `/static/` and directory `/home/домен/папкапроекта/static`
        1. Add url `/media/` and directory `/home/домен/папкапроекта/media`
1. `Edit WSGI configuration file` (click the link)
    1. Find "django" section
        1. Comment out django section
        1. Change `path` to the folder with your 'manage.py' file (`/home/домен/папкапроекта`)
        1. Change `os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'` 
        where `mysite` is the project/module/folder name with 'settings.py' file
        (`os.environ['DJANGO_SETTINGS_MODULE'] = 'proj.settings'`)

        ```python
        # My WSGI file
        # +++++++++++ DJANGO +++++++++++
        # To use your own django app use code like this:
        import os
        import sys

        # assuming your django settings file is at '/home/denniskot/mysite/mysite/settings.py'
        # and your manage.py is is at '/home/denniskot/mysite/manage.py'
        path = '/home/denniskot/django-dummy/src'
        if path not in sys.path:
            sys.path.append(path)

        os.environ['DJANGO_SETTINGS_MODULE'] = 'proj.settings'

        # then:
        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()
        ```
1. Отредактировать settings.py
    1. edit 
        ```python
        ALLOWED_HOSTS = ['yourloginname.ako.ru',]
        ```
    2. edit lines below STATIC_URL
        ```python
        # Change path in *_ROOT according to your static and media path
        MEDIA_URL = '/media/'
        STATIC_ROOT = '/home/домен/папкапроекта/static'
        MEDIA_ROOT = '/home/домен/папкапроекта/media'


