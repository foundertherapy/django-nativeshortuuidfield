import django.db.models

import native_shortuuid


class NativeUUIDSearchMixin:
    def is_valid_shortuuid(self, seach_term):
        try:
            # It's not decode-able, thus, not a shortuuid
            native_shortuuid.decode(seach_term)
        except ValueError:
            return False

        return True

    def get_search_fields(self, request):
        search_fields = super().get_search_fields(request)
        if not hasattr(self, '_uuid_search_fields'):
            self._uuid_search_fields = tuple(x for x in search_fields if x.endswith('uuid'))
            self._non_uuid_search_fields = tuple(x for x in search_fields if not x.endswith('uuid'))
        return self._non_uuid_search_fields or self._non_uuid_search_fields + ('id', )

    def get_search_results(self, request, queryset, search_term):
        # We send the search_term as None to remove the search_fields from the query and add them properly here
        queryset, use_distinct = super().get_search_results(request, queryset, search_term=None)
        field_queries = django.db.models.Q()
        if self.is_valid_shortuuid(search_term):
            for field_name_uuid in self._uuid_search_fields:
                field_queries |= django.db.models.Q(**{field_name_uuid: search_term, })

        for field_name in self._non_uuid_search_fields:
            field_queries |= django.db.models.Q(**{'{}__icontains'.format(field_name): search_term, })
        return queryset.filter(field_queries), use_distinct
