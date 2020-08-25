from zope.app.wsgi.testlayer import BrowserLayer
from zope.testbrowser.wsgi import TestBrowserLayer


class DolmenFormLayer(TestBrowserLayer, BrowserLayer):

    def wsgi_app(self):
        return self.make_wsgi_app()
