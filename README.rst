django-nativeshortuuidfield
---------------------------

|Tests| |Linters|

Provides a NativeShortUUIDField for your Django models which uses the base-57 "Short UUID" package at https://github.com/stochastic-technologies/shortuuid/ to be used in Python
and store it as full UUID in database.

Installation
============

Install it with pip (or easy_install)::

	pip install django-nativeshortuuidfield

Usage
=====

First you'll need to add a NativeShortUUIDField to your class::

	from native_shortuuid import NativeShortUUIDField

	class MyModel(models.Model):
	    uuid = NativeShortUUIDField(unique=True, default=uuid.uuid4)

Enjoy!

Notes
=====

* NativeShortUUIDField is a subclass of django.db.models.UUIDField

* You can pass usual Django UUIDField parameters on init, although some of them are added/overwritten:
    + blank=True, editable=False (set auto=False to remove these fields enforcement)

Contribution Notes
^^^^^^^^^^^^^^^^^^

Pull Request
""""""""""""
* Increase the version number in the ``setup.py`` to the new version that the new pull request represents.

Publishing the Package
"""""""""""""""""""""""""
After the pull request gets merged into the master branch a new release should be created

* Create a new tag with the same version number you updated the ``setup.py`` with::

    git checkout master
    git tag -a 2.1.0 -m 'fix importing order'
    git push origin 2.1.0

* Go to GitHub's releases section and create a new release:
    + Chose the tag version that you just created
    + Fill the release title with the same version number
    + Add a description of the release and publish it


.. |Linters| image:: https://github.com/foundertherapy/django-nativeshortuuidfield/actions/workflows/linters.yml/badge.svg
   :target: http://unmaintained.tech/
.. |Tests| image:: https://github.com/foundertherapy/django-nativeshortuuidfield/actions/workflows/tests.yml/badge.svg
   :target: http://unmaintained.tech/
