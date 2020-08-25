# -*- coding: utf-8 -*-

import unittest
import doctest
from dolmen.forms.wizard import tests


def test_suite():
    optionflags = (doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS)
    layer = tests.DolmenFormLayer(tests.test_browser)
    suite = unittest.TestSuite()

    steps = doctest.DocTestSuite(
        'dolmen.forms.wizard.tests.steps',
        extraglobs={"getRootFolder": layer.getRootFolder},
        optionflags=optionflags)
    steps.layer = layer
    suite.addTest(steps)

    rendering = doctest.DocTestSuite(
        'dolmen.forms.wizard.tests.rendering',
        extraglobs={"getRootFolder": layer.getRootFolder},
        optionflags=(doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS))
    rendering.layer = layer
    suite.addTest(rendering)

    update = doctest.DocFileSuite('wizard.txt', optionflags=optionflags)
    update.layer = layer
    suite.addTest(update)

    return suite
