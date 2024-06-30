Добро пожаловать в документацию app-template!
==================================================


Этот проект основан на шаблоне от wemake.services
и предназначен для написания django application.
Задача шаблона - обеспечить высокое качество кода и быстрый
старт при разработке новой аппы.

Можно прочитать подробности о разработке в wemake.services тут:
`our processes <https://github.com/wemake-services/meta>`_.


Ограничения
-----------

Предполагается что мы:

- Используем ``docker`` для разворачивания
- Работаем с Gitlab и Gitlab CI
- Не пишем никакого фронта на ``django``,
  фронт живет независимо.

С чего начать
-------------

С документации

Нужно понимать следующие процессы:

- Как начать писать django-app
- Как его тестировать
- Как его деплоить (выкладывать новую версию на pypi)
- Как установить локально: какие нужны зависимости,
  и как их поставить; как запустить проект у себя;
- Разработка: как делать изменения, как запускать тесты.

.. toctree::
   :maxdepth: 2
   :caption: Начало работы:

   pages/template/start-with-app.rst

.. toctree::
   :maxdepth: 2
   :caption: Установка:

   pages/template/overview.rst
   pages/template/development.rst
   pages/template/django.rst

.. toctree::
   :maxdepth: 2
   :caption: Обеспечение качества кода:

   pages/template/documentation.rst
   pages/template/linters.rst
   pages/template/testing.rst
   pages/template/security.rst
   pages/template/gitlab-ci.rst

.. toctree::
   :maxdepth: 2
   :caption: Разворачивание на прод:

   pages/template/production-checklist.rst
   pages/template/production.rst
   pages/template/packaging.rst

.. toctree::
   :maxdepth: 1
   :caption: Дополнительно:

   pages/template/upgrading-template.rst
   pages/template/faq.rst
   pages/template/troubleshooting.rst


Indexes and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
