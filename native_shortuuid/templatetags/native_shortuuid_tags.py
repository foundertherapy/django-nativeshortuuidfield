import django.contrib.admin.templatetags.admin_list
from django.template import Library

register = Library()


class InclusionNateveShortUuidNode(django.contrib.admin.templatetags.admin_list.InclusionAdminNode):
    def render(self, context):
        context.render_context[self] = context.template.engine.get_template(self.template_name)
        return super(django.contrib.admin.templatetags.admin_list.InclusionAdminNode, self).render(context)


@register.tag(name="custom_search_form")
def custom_search_form_tag(parser, token):
    """Customization of admin django.contrib.admin.templatetags.admin_list.search_form_tag"""
    inclusion_admin_node = InclusionNateveShortUuidNode(
        parser,
        token,
        func=django.contrib.admin.templatetags.admin_list.search_form,
        template_name="admin/native_shortuuid/native_shortuuid_search_form.html",
        takes_context=False,
    )
    return inclusion_admin_node
