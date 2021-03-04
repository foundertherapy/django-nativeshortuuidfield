import json
import uuid

import django.db
import django.test
from django.core import exceptions
from django.core import serializers
from django.db.models import CharField
from django.db.models import F
from django.db.models import Value
from django.db.models.functions import Concat
from django.db.models.functions import Repeat

import native_shortuuid
import shortuuid
from .models import NullableShortUUIDModel
from .models import PrimaryKeyShortUUIDModel
from .models import RelatedToShortUUIDModel
from .models import ShortUUIDGrandchild
from .models import ShortUUIDModel


class TestSaveLoad(django.test.TestCase):
    def test_shortuuid_instance(self):
        instance = ShortUUIDModel.objects.create(field=shortuuid.encode(uuid.uuid4()))
        loaded = ShortUUIDModel.objects.get()
        self.assertEqual(loaded.field, instance.field)

    def test_null_handling(self):
        NullableShortUUIDModel.objects.create(field=None)
        loaded = NullableShortUUIDModel.objects.get()
        self.assertIsNone(loaded.field)

    def test_pk_validated(self):
        with self.assertRaisesMessage(exceptions.ValidationError, 'is not a valid ShortUUID'):
            PrimaryKeyShortUUIDModel.objects.get(pk={})

        with self.assertRaisesMessage(exceptions.ValidationError, 'is not a valid ShortUUID'):
            PrimaryKeyShortUUIDModel.objects.get(pk=[])

    def test_wrong_value(self):
        with self.assertRaisesMessage(exceptions.ValidationError, 'is not a valid ShortUUID'):
            ShortUUIDModel.objects.get(field='not-a-shortuuid')

        with self.assertRaisesMessage(exceptions.ValidationError, 'is not a valid ShortUUID'):
            ShortUUIDModel.objects.create(field='not-a-shortuuid')

        with self.assertRaisesMessage(exceptions.ValidationError, 'is not a valid ShortUUID'):
            ShortUUIDModel.objects.create(field='0f3990cf-25be-47bc-bc69-41a0c9e09d86')

        with self.assertRaisesMessage(exceptions.ValidationError, 'is not a valid ShortUUID'):
            ShortUUIDModel.objects.create(field=(2 ** 128) - 1)

    def test_wrong_characters_for_shortuuid_value(self):
        """ShortUUID should not contain l, 1, I, O or 0 character."""

        # ShortUUID should not contain l character.
        with self.assertRaisesMessage(exceptions.ValidationError, 'is not a valid ShortUUID'):
            ShortUUIDModel.objects.create(field='5QaMgroc94l9xa2GdSwDzL')

        # ShortUUID should not contain 1 character.
        with self.assertRaisesMessage(exceptions.ValidationError, 'is not a valid ShortUUID'):
            ShortUUIDModel.objects.create(field='5QaMgroc9419xa2GdSwDzL')

        # ShortUUID should not contain I character.
        with self.assertRaisesMessage(exceptions.ValidationError, 'is not a valid ShortUUID'):
            ShortUUIDModel.objects.create(field='5QaMgroc94I9xa2GdSwDzL')

        # ShortUUID should not contain O character.
        with self.assertRaisesMessage(exceptions.ValidationError, 'is not a valid ShortUUID'):
            ShortUUIDModel.objects.create(field='5QaMgroc94O9xa2GdSwDzL')

        # ShortUUID should not contain 0 character.
        with self.assertRaisesMessage(exceptions.ValidationError, 'is not a valid ShortUUID'):
            ShortUUIDModel.objects.create(field='5QaMgroc9409xa2GdSwDzL')


class TestMethods(django.test.SimpleTestCase):

    def test_deconstruct(self):
        field = native_shortuuid.NativeShortUUIDField()
        name, path, args, kwargs = field.deconstruct()
        self.assertEqual(kwargs, {})

        field = native_shortuuid.NativeShortUUIDField(default=native_shortuuid.fields.short_uuid4)
        name, path, args, kwargs = field.deconstruct()
        self.assertEqual(set(kwargs.keys()), {'default'})
        self.assertEqual(kwargs['default'], native_shortuuid.fields.short_uuid4)

        field = native_shortuuid.NativeShortUUIDField(default=uuid.uuid4)
        name, path, args, kwargs = field.deconstruct()
        self.assertEqual(set(kwargs.keys()), {'default'})
        self.assertEqual(kwargs['default'], uuid.uuid4)

    def test_to_python(self):
        self.assertIsNone(native_shortuuid.NativeShortUUIDField().to_python(None))

    def test_to_python_shortuuid_too_large(self):
        # Fails for strings larger than 22 characters.
        with self.assertRaises(exceptions.ValidationError):
            native_shortuuid.NativeShortUUIDField().to_python('2' * 23)

    def test_to_python_shortuuid_too_small(self):
        # Fails for strings less than 22 characters.
        with self.assertRaises(exceptions.ValidationError):
            native_shortuuid.NativeShortUUIDField().to_python('2' * 21)


class TestQuerying(django.test.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.objs = [
            NullableShortUUIDModel.objects.create(field='8jeD2ws9cvwC3jEhyZCz8E'),
            NullableShortUUIDModel.objects.create(field='H9cNmGXLE6446655442222'),
            NullableShortUUIDModel.objects.create(field=None),
        ]

    def test_exact(self):
        self.assertSequenceEqual(
            NullableShortUUIDModel.objects.filter(field__exact='H9cNmGXLE6446655442222'),
            [self.objs[1]]
        )

    def test_iexact(self):
        # iexact uses the UUID rather tan the ShortUUID
        self.assertSequenceEqual(
            NullableShortUUIDModel.objects.filter(field__iexact='550e8400-e29b-3a56-e212-4d8b73e7390a'),
            [self.objs[1]],
        )
        self.assertSequenceEqual(
            NullableShortUUIDModel.objects.filter(field__iexact='550e8400e29b3a56e2124d8b73e7390a'),
            [self.objs[1]],
        )

    def test_isnull(self):
        self.assertSequenceEqual(
            NullableShortUUIDModel.objects.filter(field__isnull=True),
            [self.objs[2]]
        )

    def test_contains(self):
        # contains uses the UUID rather tan the ShortUUID
        self.assertSequenceEqual(
            NullableShortUUIDModel.objects.filter(field__contains='8400e29b'),
            [self.objs[1]],
        )
        self.assertSequenceEqual(
            NullableShortUUIDModel.objects.filter(field__contains='550e-8400'),
            [self.objs[1]],
        )

    def test_icontains(self):
        # icontains uses the UUID rather tan the ShortUUID
        self.assertSequenceEqual(
            NullableShortUUIDModel.objects.filter(field__icontains='8400E29B'),
            [self.objs[1]],
        )
        self.assertSequenceEqual(
            NullableShortUUIDModel.objects.filter(field__icontains='550E-8400'),
            [self.objs[1]],
        )

    def test_startswith(self):
        # startswith uses the UUID rather tan the ShortUUID
        self.assertSequenceEqual(
            NullableShortUUIDModel.objects.filter(field__startswith='550e8400e29b3'),
            [self.objs[1]],
        )
        self.assertSequenceEqual(
            NullableShortUUIDModel.objects.filter(field__startswith='550e8400-e29b-3'),
            [self.objs[1]],
        )

    def test_istartswith(self):
        # istartswith uses the UUID rather tan the ShortUUID
        self.assertSequenceEqual(
            NullableShortUUIDModel.objects.filter(field__istartswith='550E8400E29B3'),
            [self.objs[1]],
        )
        self.assertSequenceEqual(
            NullableShortUUIDModel.objects.filter(field__istartswith='550E8400-E29B-3'),
            [self.objs[1]],
        )

    def test_endswith(self):
        # endswith uses the UUID rather tan the ShortUUID
        self.assertSequenceEqual(
            NullableShortUUIDModel.objects.filter(field__endswith='e2124d8b73e7390a'),
            [self.objs[1]],
        )
        self.assertSequenceEqual(
            NullableShortUUIDModel.objects.filter(field__endswith='e212-4d8b73e7390a'),
            [self.objs[1]],
        )

    def test_iendswith(self):
        # iendswith uses the UUID rather tan the ShortUUID
        self.assertSequenceEqual(
            NullableShortUUIDModel.objects.filter(field__iendswith='E2124D8B73E7390A'),
            [self.objs[1]],
        )
        self.assertSequenceEqual(
            NullableShortUUIDModel.objects.filter(field__iendswith='E212-4D8B73E7390A'),
            [self.objs[1]],
        )

    def test_filter_with_expr(self):
        # contains uses the UUID rather tan the ShortUUID
        self.assertSequenceEqual(
            NullableShortUUIDModel.objects.annotate(
                value=Concat(Value('8400'), Value('e29b'), output_field=CharField()),
            ).filter(field__contains=F('value')),
            [self.objs[1]],
        )
        self.assertSequenceEqual(
            NullableShortUUIDModel.objects.annotate(
                value=Concat(Value('8400'), Value('-'), Value('e29b'), output_field=CharField()),
            ).filter(field__contains=F('value')),
            [self.objs[1]],
        )
        self.assertSequenceEqual(
            NullableShortUUIDModel.objects.annotate(
                value=Repeat(Value('0'), 2, output_field=CharField()),
            ).filter(field__contains=F('value')),
            [self.objs[1]],
        )


class TestSerialization(django.test.SimpleTestCase):
    test_data = (
        '[{"fields": {"field": "H9cNmGXLE6446655442222"}, '
        '"model": "tests.shortuuidmodel", "pk": null}]'
    )
    nullable_test_data = (
        '[{"fields": {"field": null}, '
        '"model": "tests.nullableshortuuidmodel", "pk": null}]'
    )

    def test_dumping(self):
        instance = ShortUUIDModel(field='H9cNmGXLE6446655442222')
        data = serializers.serialize('json', [instance])
        self.assertEqual(json.loads(data), json.loads(self.test_data))

    def test_loading(self):
        # deserialize uses UUIDs
        instance = list(serializers.deserialize('json', self.test_data))[0].object
        self.assertEqual(instance.field, uuid.UUID('550e8400-e29b-3a56-e212-4d8b73e7390a'))

    def test_nullable_loading(self):
        instance = list(serializers.deserialize('json', self.nullable_test_data))[0].object
        self.assertIsNone(instance.field)


class TestValidation(django.test.SimpleTestCase):
    def test_invalid_uuid(self):
        field = native_shortuuid.NativeShortUUIDField()
        with self.assertRaises(exceptions.ValidationError) as cm:
            field.clean('550e8400', None)
        self.assertEqual(cm.exception.code, 'invalid')
        self.assertEqual(cm.exception.message % cm.exception.params, '“550e8400” is not a valid ShortUUID.')

    def test_uuid_instance_ok(self):
        field = native_shortuuid.NativeShortUUIDField()
        field.clean(shortuuid.encode(uuid.uuid4()), None)  # no error
        field.clean(uuid.uuid4(), None)  # no error


class TestAsPrimaryKey(django.test.TestCase):
    def test_creation(self):
        PrimaryKeyShortUUIDModel.objects.create()
        loaded = PrimaryKeyShortUUIDModel.objects.get()
        self.assertIsInstance(loaded.pk, str)
        self.assertIsInstance(native_shortuuid.decode(loaded.pk), uuid.UUID)

    def test_shortuuid_pk_on_save(self):
        saved = PrimaryKeyShortUUIDModel.objects.create(id=None)
        loaded = PrimaryKeyShortUUIDModel.objects.get()
        self.assertIsNotNone(loaded.id)
        self.assertEqual(loaded.id, saved.id)

    def test_uuid_pk_on_bulk_create(self):
        u1 = PrimaryKeyShortUUIDModel()
        u2 = PrimaryKeyShortUUIDModel(id=None)
        PrimaryKeyShortUUIDModel.objects.bulk_create([u1, u2])
        # The two objects were correctly created.
        u1_found = PrimaryKeyShortUUIDModel.objects.filter(id=u1.id).exists()
        u2_found = PrimaryKeyShortUUIDModel.objects.exclude(id=u1.id).exists()
        self.assertTrue(u1_found)
        self.assertTrue(u2_found)
        self.assertEqual(PrimaryKeyShortUUIDModel.objects.count(), 2)

    def test_underlying_field(self):
        pk_model = PrimaryKeyShortUUIDModel.objects.create()
        RelatedToShortUUIDModel.objects.create(shortuuid_fk=pk_model)
        related = RelatedToShortUUIDModel.objects.get()
        self.assertEqual(related.shortuuid_fk.pk, related.shortuuid_fk_id)

    def test_update_with_related_model_instance(self):
        # regression for #24611
        u1 = PrimaryKeyShortUUIDModel.objects.create()
        u2 = PrimaryKeyShortUUIDModel.objects.create()
        r = RelatedToShortUUIDModel.objects.create(shortuuid_fk=u1)
        RelatedToShortUUIDModel.objects.update(shortuuid_fk=u2)
        r.refresh_from_db()
        self.assertEqual(r.shortuuid_fk, u2)

    def test_update_with_related_model_id(self):
        u1 = PrimaryKeyShortUUIDModel.objects.create()
        u2 = PrimaryKeyShortUUIDModel.objects.create()
        r = RelatedToShortUUIDModel.objects.create(shortuuid_fk=u1)
        RelatedToShortUUIDModel.objects.update(shortuuid_fk=u2.pk)
        r.refresh_from_db()
        self.assertEqual(r.shortuuid_fk, u2)

    def test_two_level_foreign_keys(self):
        gc = ShortUUIDGrandchild()
        # exercises ForeignKey.get_db_prep_value()
        gc.save()
        self.assertIsInstance(gc.shortuuidchild_ptr_id, str)
        self.assertIsInstance(native_shortuuid.decode(gc.shortuuidchild_ptr_id), uuid.UUID)
        gc.refresh_from_db()
        self.assertIsInstance(gc.shortuuidchild_ptr_id, str)
        self.assertIsInstance(native_shortuuid.decode(gc.shortuuidchild_ptr_id), uuid.UUID)


class TestAsPrimaryKeyTransactionTests(django.test.TransactionTestCase):
    # Need a TransactionTestCase to avoid deferring FK constraint checking.
    available_apps = ['tests']

    @django.test.skipUnlessDBFeature('supports_foreign_keys')
    def test_unsaved_fk(self):
        u1 = PrimaryKeyShortUUIDModel()
        with self.assertRaises(django.db.IntegrityError):
            RelatedToShortUUIDModel.objects.create(shortuuid_fk=u1)
