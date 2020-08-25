#!/usr/bin/python
# -*- coding: utf-8 -*-

from zeam.form.composed import view

# Message Factory
from zope.i18nmessageid import MessageFactory
MF = MessageFactory('dolmen.forms.wizard')

# Exposing package API
from dolmen.forms.wizard.wizard import Wizard, WizardStep
