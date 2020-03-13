django-nativeshortuuidfield
----------------

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
