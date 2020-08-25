import grokcore.component
import grokcore.view
import martian

from grokcore.view.meta.views import default_view_name
from dolmen.forms.wizard.interfaces import IStep
from dolmen.forms.wizard.wizard import Wizard, WizardStep
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class StepGrokker(martian.ClassGrokker):
    """Grokker to register sub forms.
    """
    martian.component(WizardStep)
    martian.directive(grokcore.component.context)
    martian.directive(grokcore.view.layer, default=IDefaultBrowserLayer)
    martian.directive(grokcore.view.view)
    martian.directive(grokcore.view.name, get_default=default_view_name)

    def grok(self, name, factory, module_info, **kw):
        factory.module_info = module_info
        return super().grok(name, factory, module_info, **kw)

    def execute(self, factory, config, context, layer, view, name, **kw):

        if not factory.__dict__.get('prefix'):
            factory.prefix = '%s.%s' % (view.prefix, name)

        adapts = (context, view, layer)
        config.action(
            discriminator=('adapter', adapts, IStep, name),
            callable=grokcore.component.util.provideAdapter,
            args=(factory, adapts, IStep, name),
        )
        return True
