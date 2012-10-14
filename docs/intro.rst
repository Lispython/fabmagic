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

