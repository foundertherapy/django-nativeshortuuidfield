# django-nativeshortuuidfield

[![Tests](https://github.com/foundertherapy/django-nativeshortuuidfield/actions/workflows/tests.yml/badge.svg)](https://github.com/foundertherapy/django-nativeshortuuidfield/actions/workflows/tests.yml)
[![Linters](https://github.com/foundertherapy/django-nativeshortuuidfield/actions/workflows/linters.yml/badge.svg)](https://github.com/foundertherapy/django-nativeshortuuidfield/actions/workflows/linters.yml)

Provides a NativeShortUUIDField for your Django models which uses the base-57 "Short UUID" package at https://github.com/stochastic-technologies/shortuuid/ to be used in Python
and store it as full UUID in database.

## Installation

Install it with pip (or easy_install):
```bash
$ pip install django-nativeshortuuidfield
```

## Usage

First you'll need to add a NativeShortUUIDField to your class:
```python
from native_shortuuid import NativeShortUUIDField

class MyModel(models.Model):
    uuid = NativeShortUUIDField(unique=True, default=uuid.uuid4)
```

If you want to add the ability to search by shortuuid in `ModelAdmin` you need to inherit `NativeUUIDSearchMixin`
```python
from native_shortuuid.admin import NativeUUIDSearchMixin

@admin.register(models.MyModel)
class MyModelAdmin(NativeUUIDSearchMixin, admin.ModelAdmin):
    search_fields = ('uuid', )
``` 

If you want to have to ability to write your own uuid search fields list
```python
from native_shortuuid.admin import NativeUUIDSearchMixin

@admin.register(models.MyModel)
class MyModelAdmin(NativeUUIDSearchMixin, admin.ModelAdmin):
    admin_auto_extract_uuid_search_fields = False
    search_fields = ('name', )
    search_uuid_fields = ['uuid', 'foreign_model__uuid']
``` 


Enjoy!

## Settings
* `ADMIN_AUTO_EXTRACT_UUID_SEARCH_FIELDS`: default `True`
    + This setting is to autofill `search_uuid_fields` in the ModelAdmins that inherits `NativeUUIDSearchMixin` 
    with all shortuuid fields that are in the `search_fields` array.
    if you turned it off, you'll need to define `search_uuid_fields` on you ModelAdmin in order to search on shortuuid fields
    
## Notes

* NativeShortUUIDField is a subclass of django.db.models.UUIDField

* You can pass usual Django UUIDField parameters on init, although some of them are added/overwritten:
    + blank=True, editable=False (set auto=False to remove these fields enforcement)

### Contribution Notes

#### Pull Request
* Increase the version number in the `setup.py` to the new version that the new pull request represents.

#### Publishing the Package
After the pull request gets merged into the master branch a new release should be created

* Create a new tag with the same version number you updated the `setup.py` with:
    ```bash
    $ git checkout master
    $ git tag -a 2.1.0 -m 'fix importing order'
    $ git push origin 2.1.0
    ```

* Go to GitHub's releases section and create a new release:
    + Chose the tag version that you just created
    + Fill the release title with the same version number
    + Add a description of the release and publish it
