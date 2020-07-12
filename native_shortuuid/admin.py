import shortuuid


class NativeUUIDSearchMixin:
    def get_search_fields(self, request):
        search_fields = super().get_search_fields(request)
        if not hasattr(self, '_uuid_search_fields'):
            self._uuid_search_fields = tuple(x for x in search_fields if x.endswith('uuid'))
            self._non_uuid_search_fields = tuple(x for x in search_fields if not x.endswith('uuid'))
        return self._non_uuid_search_fields or self._non_uuid_search_fields + ('id', )

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        try:
            search_term_as_uuid = shortuuid.decode(search_term.strip())
        except ValueError as e:
            pass
        else:
            for uuid_search_field in self._uuid_search_fields:
                search_params = {
                    uuid_search_field: search_term_as_uuid,
                }
                queryset |= self.model.objects.filter(**search_params)
        return queryset, use_distinct
