import uuid

import django.db.models

import native_shortuuid


class ShortUUIDModel(django.db.models.Model):
    field = native_shortuuid.NativeShortUUIDField()


class ShortUUID20Model(django.db.models.Model):
    field = native_shortuuid.NativeShortUUID20Field()


class NullableShortUUIDModel(django.db.models.Model):
    field = native_shortuuid.NativeShortUUIDField(blank=True, null=True)


class NullableShortUUID20Model(django.db.models.Model):
    field = native_shortuuid.NativeShortUUID20Field(blank=True, null=True)


class PrimaryKeyShortUUIDModel(django.db.models.Model):
    id = native_shortuuid.NativeShortUUIDField(primary_key=True, default=uuid.uuid4)


class PrimaryKeyShortUUID20Model(django.db.models.Model):
    id = native_shortuuid.NativeShortUUID20Field(primary_key=True, default=native_shortuuid.fields.uuid4_12bits_masked)


class RelatedToShortUUIDModel(django.db.models.Model):
    shortuuid_fk = django.db.models.ForeignKey('PrimaryKeyShortUUIDModel', django.db.models.CASCADE)


class RelatedToShortUUID20Model(django.db.models.Model):
    shortuuid_fk = django.db.models.ForeignKey('PrimaryKeyShortUUID20Model', django.db.models.CASCADE)


class ShortUUIDChild(PrimaryKeyShortUUIDModel):
    pass


class ShortUUID20Child(PrimaryKeyShortUUID20Model):
    pass


class ShortUUIDGrandchild(ShortUUIDChild):
    pass


class ShortUUID20Grandchild(ShortUUID20Child):
    pass
