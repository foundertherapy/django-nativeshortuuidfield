import django.contrib.admin.templatetags.admin_list
from django.template import Library

register = Library()


@register.tag(name="custom_search_form")
def custom_search_form_tag(parser, token):
    inclusion_admin_node = django.contrib.admin.templatetags.admin_list.search_form_tag(parser, token)
    inclusion_admin_node.template_name = "native_shortuuid_search_form.html"
    return inclusion_admin_node
