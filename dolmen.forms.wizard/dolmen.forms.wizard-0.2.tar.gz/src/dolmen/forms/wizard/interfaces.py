# -*- coding: utf-8 -*-

from zope import interface


class IWizard(interface.Interface):
    """Marker interface for Form wizards
    """

class IStep(interface.Interface):
    """Marker interface for Wizard Steps
    """


class IUpdatableForm(interface.Interface):
    """This interface defines a form that can be updated.
    """

    def updateContentData(data):
        """Update content data.
        """
