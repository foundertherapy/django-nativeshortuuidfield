import django.conf
import django.db.models

import native_shortuuid


class NativeUUIDSearchMixin:
    search_uuid_fields = []
    admin_auto_extract_uuid_search_fields = True  # To customize a specific admins instead of all

    def is_valid_shortuuid(self, search_term):
        try:
            # It's not decode-able, thus, not a shortuuid
            native_shortuuid.decode(search_term)
        except ValueError:
            return False

        return True

    def is_model_field_native_short_uuid(self, search_field):
        model_field = next((field for field in self.model._meta.fields if field.attname == search_field), None)
        return model_field and isinstance(model_field, native_shortuuid.NativeShortUUIDField)

    def get_search_fields(self, request):
        search_fields = list(super().get_search_fields(request) or [])
        if getattr(django.conf.settings, 'ADMIN_AUTO_EXTRACT_UUID_SEARCH_FIELDS', True) \
                and self.admin_auto_extract_uuid_search_fields:
            for search_field in search_fields:
                if self.is_model_field_native_short_uuid(search_field) or search_field.endswith('uuid'):
                    self.search_uuid_fields.append(search_field)
                    search_fields.remove(search_field)
        return search_fields or ('id',)

    def get_search_results(self, request, queryset, search_term):
        results_queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        field_queries = django.db.models.Q()
        if self.search_uuid_fields and search_term and self.is_valid_shortuuid(search_term):
            for field_name_uuid in self.search_uuid_fields:
                field_queries |= django.db.models.Q(**{field_name_uuid: search_term})
            return queryset.filter(field_queries), use_distinct

        return results_queryset, use_distinct
