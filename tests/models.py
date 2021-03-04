import uuid

import django.db.models

import native_shortuuid


class ShortUUIDModel(django.db.models.Model):
    field = native_shortuuid.NativeShortUUIDField()


class NullableShortUUIDModel(django.db.models.Model):
    field = native_shortuuid.NativeShortUUIDField(blank=True, null=True)


class PrimaryKeyShortUUIDModel(django.db.models.Model):
    id = native_shortuuid.NativeShortUUIDField(primary_key=True, default=uuid.uuid4)


class RelatedToShortUUIDModel(django.db.models.Model):
    shortuuid_fk = django.db.models.ForeignKey('PrimaryKeyShortUUIDModel', django.db.models.CASCADE)


class ShortUUIDChild(PrimaryKeyShortUUIDModel):
    pass


class ShortUUIDGrandchild(ShortUUIDChild):
    pass
