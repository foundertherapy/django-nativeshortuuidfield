import django.conf
import django.db.models

import native_shortuuid


class NativeUUIDSearchMixin:
    search_uuid_fields = []

    def is_valid_shortuuid(self, search_term):
        try:
            # It's not decode-able, thus, not a shortuuid
            native_shortuuid.decode(search_term)
        except ValueError:
            return False

        return True

    def get_search_fields(self, request):
        search_fields = list(super().get_search_fields(request) or [])
        if getattr(django.conf.settings, 'ADMIN_AUTO_EXTRACT_UUID_SEARCH_FIELDS', True):
            self.search_uuid_fields = []
            for field in self.model._meta.fields:
                if field.attname in search_fields and isinstance(field, native_shortuuid.NativeShortUUIDField):
                    self.search_uuid_fields.append(field.attname)
                    search_fields.remove(field.attname)
        return search_fields or ('id',)

    def get_search_results(self, request, queryset, search_term):
        results_queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        field_queries = django.db.models.Q()
        if self.search_uuid_fields and search_term and self.is_valid_shortuuid(search_term):
            for field_name_uuid in self.search_uuid_fields:
                field_queries |= django.db.models.Q(**{field_name_uuid: search_term})
            return queryset.filter(field_queries), use_distinct

        return results_queryset, use_distinct
