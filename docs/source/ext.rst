.. module:: fabmagic

Fabmagic extensions
-------------------

Fabric Magic extensions extent the functionality of Fabric Magic recipes.


Installation extension
~~~~~~~~~~~~~~~~~~~~~~

You can install extension with `easy_install`_ or `pip`_::

    easy_install fabmagic-extenstion
    pip install fabmagic-extension


.. _easy_install: http://peak.telecommunity.com/DevCenter/EasyInstall
.. _pip: http://pypi.python.org/pypi/pip


Usage
~~~~~

To user Fabric Magic Recipes extension add it's to configuration list


.. sourcecode:: python

    import fabmagic
    fabmagic.configure_recipes(
        "nginx",
        "ext.extension")


