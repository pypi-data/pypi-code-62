import grokcore.component as grok
from grokcore.component.util import sort_components

from megrok import pagetemplate as pt
from zeam.form import base
from zeam.form.base import Actions
from zeam.form.base.form import FormCanvas, GrokViewSupport
from zeam.form.base.widgets import getWidgetExtractor
from zope.interface import implementer
from zope.component import getAdapters

from dolmen.forms.wizard import MF as _
from dolmen.forms.wizard.interfaces import IWizard, IStep
from dolmen.forms.wizard.actions import (PreviousAction, SaveAction,
    NextAction, HiddenSaveAction)


pt.templatedir('default_templates')


@implementer(IWizard)
class Wizard(base.Form):
    grok.baseclass()

    ignoreRequest = True
    ignoreContent = False

    fields = base.Fields(base.Field("Step"))
    fields['step'].mode = base.HIDDEN
    fields['step'].defaultValue = 0

    actions = base.Actions(
        PreviousAction(_(u"Back")),
        SaveAction(_(u"Save")),
        NextAction(_(u"Continue")))

    def __init__(self, context, request):
        super().__init__(context, request)
        self.setContentData(self)

        steps = (f[1] for f in getAdapters(
            (self.context, self,  self.request), IStep))

        self.allSteps = sort_components(steps)
        self.__extracted_step = False

    def finish(self):
        """After-save hook.
        """
        return

    def getMaximumStepId(self):
        """Returns the maximum step id.
        """
        return len(self.allSteps) - 1

    def getStep(self, identifier):
        for form in self.steps:
            if form.htmlId() == identifier:
                return form
        return None

    def getCurrentStepId(self):
        """Returns the current step id.
        """
        if self.__extracted_step is True:
            return int(self.step)

        value, error = getWidgetExtractor(
            self.fields['step'], self, self.request).extract()

        if value is base.NO_VALUE:
            value = 0
        else:
            value = int(value)

        if value < 0 or value > self.getMaximumStepId():
            value = 0
        self.step = value
        self.__extracted_step = True
        return value

    def setCurrentStep(self, sid):
        """Sets a new current step.
        """
        sid = int(sid)
        if not self.allSteps:
            self.current = None
            self.step = sid
        else:
            try:
                assert sid >= 0 and sid < len(self.allSteps)
            except AssertionError as e:
                raise AssertionError(
                    'Value %r is not within the permitted range' % sid)
            self.step = sid
            self.current = self.allSteps[sid]

    def updateForm(self):
        self.setCurrentStep(self.getCurrentStepId())
        base.Form.updateActions(self)
        self.current.updateWidgets()
        base.Form.updateWidgets(self)

    def update(self):
        pass


class WizardTemplate(pt.PageTemplate):
    pt.view(Wizard)


class WizardStep(FormCanvas, GrokViewSupport):
    pt.view(Wizard)
    grok.baseclass()

    actions = Actions(
        HiddenSaveAction(_(u"Save")))

    # Set prefix to None, so it's changed by the grokker
    label = u''
    description = u''
    prefix = None

    def __init__(self, context, parent, request):
        super().__init__(context, request)
        self.parent = parent

    def available(self):
        return True

    def htmlId(self):
        return self.prefix.replace('.', '-')

    def getWizard(self):
        return self.parent


class StepTemplate(pt.PageTemplate):
    pt.view(WizardStep)


__all__ = ["Wizard", "WizardStep", "Fields",
           "Action", "Actions", "FAILURE", "SUCCESS"]
