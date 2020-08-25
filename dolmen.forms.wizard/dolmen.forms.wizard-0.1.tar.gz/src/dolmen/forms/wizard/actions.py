# -*- coding: utf-8 -*-

from zeam.form import base
from zeam.form.ztk.actions import EditAction
from zeam.form.base.markers import SUCCESS, FAILURE
from zeam.form.base.datamanager import DictDataManager

from dolmen.forms.wizard import MF as _
from dolmen.forms.wizard.interfaces import IUpdatableForm


class NextAction(base.Action):
    """Action to move to the next step.
    """

    def available(self, form):
        return form.getCurrentStepId() < form.getMaximumStepId()

    def __call__(self, form):
        if form.current.actions['save'](form.current) is SUCCESS:
            step = form.getCurrentStepId()
            form.setCurrentStep(step + 1)
            return SUCCESS
        return FAILURE


class PreviousAction(base.Action):
    """Action to move to the previous step.
    """

    def available(self, form):
        return form.getCurrentStepId() != 0

    def __call__(self, form):
        step = form.getCurrentStepId()
        form.setCurrentStep(step - 1)
        return SUCCESS


class SaveAction(EditAction):
    """Edit and redirect the user somewhere:
    """

    def __init__(self, title, url="index"):
        super(SaveAction, self).__init__(title)
        self.redirect_url = url

    def available(self, form):
        return form.getCurrentStepId() == form.getMaximumStepId()

    def __call__(self, form):
        if super(SaveAction, self).__call__(form) is SUCCESS:
            errors = form.finish()
            if not errors:
                form.redirect(form.url(self.redirect_url))
                return SUCCESS
        form.errors = errors
        return FAILURE


class HiddenSaveAction(EditAction):
    """Hidden Save Action
    """

    def available(self, form):
        return False


class UpdateAction(base.Action):
    """Update data in a form.
    """

    def available(self, form):
        return IUpdatableForm.providedBy(form)

    def __call__(self, form):
        data, errors = form.extractData()
        if errors:
            return FAILURE
        form.updateContentData(data)
        form.setContentData(DictDataManager(data))
        form.ignoreRequest = True
        form.status = _(u"Data updated.")
        return SUCCESS
