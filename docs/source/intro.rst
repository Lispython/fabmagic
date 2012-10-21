.. module:: fabmagic


Intro
-----

To use Fabric Magic Recipes you need configure recipes in your fabfile


.. sourcecode:: python

   import fabmagic

   fabmagic.configure_recipes(
       ('nginx', {"roles": ["web1", "web2", "web3"]}),
       "monit",
       "deploy")



And you can run command in you console:

.. sourcecode:: sh

    $ fab --list

    Available commands:

        configure_env                      Configure environment from YAML file
	create_env                         Create default environment file
	show_recipes                       Show available recipes
	frameworks.django.create_settings  Create django config
	frameworks.django.syncdb           Sync database
	monit.create_config                Create monit configs
	monit.restart                      Restart monit
	monit.start                        Start monit
	monit.stop                         Stop monit
	nginx.reload                       Reload nginx configs
	nginx.start                        Start nginx
	nginx.status                       Nginx status
	nginx.stop                         Stop nginx



Новая концепция работы
~~~~~~~~~~~~~~~~~~~~~~

Fabric Magic включает в себя 2 слабосвязанных компонента:

- Модуль, отвечающий за настройку кластера серверов с учетом их ролей
- Модуль, отвечающий за обновление проекта, deploy.


Настройка серверов
==================

Концепция работы модуля, занимающегося настройкой серверов.

- Обновление может быть запущено с хост-машины администратора
- Обновление может быть запущено автоматически через демона автообновления,
  в настройсках которого прописана роль машины.


Последовательность обновления с хост машины.
1. Создаем репозиторий с рецептами.
2. Создаем в нем директорию с ролями и директорию с cookbooks.
3. Создаем или генерируем fabfile.py в котором описываем, ip адреса машины, их роли



Structure
~~~~~~~~~

Global cookbooks and roles container is cookbooks-library. It's include cookbooks with recipes, roles.

* cookbooks-library:
  - cookbooks
    + nginx
      - recipes:
        * __init__.py - default recipe
        * some.py - some recipe
    + memcached
    + postgres
    + application1
  - roles
    + web [web.py] - store role name, default attributes, run_list
    + db [db.py]
