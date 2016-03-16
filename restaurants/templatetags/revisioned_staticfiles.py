from django import template
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.staticfiles.templatetags.staticfiles import StaticFilesNode

register = template.Library()


class FileRevNode(StaticFilesNode):
    """ Overrides normal static file handling by first checking for file revisions in
    settings.FILEREVS, before falling back to the actual requested filename. Otherwise
    indentical to normal static tag.
    """

    def url(self, context):
        return revisioned_static_url(self.path.resolve(context))


@register.tag
def static(parser, token):
    return FileRevNode.handle_token(parser, token)


def revisioned_static_url(path):
    path_prefix = 'static/'
    rev_path = settings.FILEREVS.get(path_prefix + path)
    if rev_path is not None:
        return staticfiles_storage.url(rev_path[len(path_prefix):])
    else:
        return staticfiles_storage.url(path)
