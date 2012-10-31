# -*- coding: utf-8 -*-
from hyde.plugin import Plugin
from hyde.site import Resource
from jinja2 import contextfunction, Markup
from jinja2.utils import pformat
from babel import support
import locale

@contextfunction
def datetime(context, val, fmt=False):
    import locale, datetime
    fmt = fmt if fmt else locale.nl_langinfo(locale.D_T_FMT)
    result = val.strftime(fmt)
    return Markup(result.decode('utf-8'))

class i18NPlugin(Plugin):

    @property
    def plugin_name(self):
        return 'i18N'

    def template_loaded(self, template):
        self.template = template
        self.resourcesById = {}
        template.env.globals['datetime'] = datetime
        template.env.add_extension('jinja2.ext.i18n')
        self.translations = {}
        for lc in self.settings.locales:
            trans = support.Translations.load(
                        dirname=self.site.sitepath.child('strings'),
                        locales=lc)
            self.translations[lc] = trans

    def begin_site(self):
        """
        Initialize plugin. Build the language tree for each node
        """
        def locale_url(self, lc):
            return self.full_url.replace('/' + self.meta.lc + '/', '/' + lc + '/')

        Resource.locale_url = locale_url

        # Build association between UUID and list of resources
        for resource in self.site.content.walk_resources():
            try:
                uuid = resource.meta.uuid
                language = resource.meta.lc
            except AttributeError:
                continue
            if uuid not in self.resourcesById:
                self.resourcesById[uuid] = []
            self.resourcesById[uuid].append(resource)
            resource.translations = self.resourcesById[uuid]

    def begin_text_resource(self, resource, text):
        try:
            lc = resource.meta.lc
            self.default_locale = locale.getlocale()
            locale.setlocale(locale.LC_ALL,
                                (lc, resource.meta.encoding))
            self.template.env.install_gettext_translations(
                self.translations[lc],
                newstyle=True)
        except AttributeError: pass
        return text

    def end_text_resource(self, resource, text):
        try:
            lc = resource.meta.lc
            locale.setlocale(locale.LC_ALL, self.default_locale)
        except AttributeError: pass
        self.template.env.uninstall_gettext_translations()
        return text