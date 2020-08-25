"""
  >>> from grokcore.component import testing
  >>> testing.grok(__name__)

We setup some content for the Wizard:

  >>> root = getRootFolder() 
  >>> root['contact'] = contact = MyContent()

  >>> from zope.testbrowser.wsgi import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
 
Let's call the 'First Step' of the Wizard with the Test-Browser:

  >>> browser.open('http://127.0.0.1/contact/personwizard')
  >>> 'Step Name' in browser.contents
  True

  >>> surname = browser.getControl(name='form.step1.field.surname')
  >>> surname
  <Control name='form.step1.field.surname' type='text'>
  >>> surname.value = 'Christian Klinger'

  >>> browser.getControl(name="form.action.continue").click()

After submitting the 'First Step' we should reach the second one:

  >>> 'Step Age' in browser.contents
  True

  >>> back = browser.getControl(name="form.action.back")
  >>> back
  <SubmitControl name='form.action.back' type='submit'>

  >>> age = browser.getControl(name="form.step2.field.age")
  >>> age
  <Control name='form.step2.field.age' type='number'>

  >>> age.value = "eight"

Obviously the value of age should be an int. So we should get an error,
But on the back button we don't get error messages.:

  >>> back.click()
  >>> "Step Name" in browser.contents
  True

Now we can navigate again to "Step Age" in try to submit the wizard
  
  >>> browser.getControl(name="form.action.continue").click()
  >>> save = browser.getControl(name="form.action.save")
  >>> save
  <SubmitControl name='form.action.save' type='submit'>

  >>> save.click()
  Finish Action: Christian Klinger 10
  >>> print(browser.contents)
  name: Christian Klinger; age: 10 
  
"""

from zeam.form.base import Fields
from dolmen.forms import wizard
from grokcore import component as grok
from grokcore import view as view
from grokcore.layout import Layout
from zope import interface
from zope import schema
from zope.security.protectclass import protectName, protectSetAttribute


class IContact(interface.Interface):
    surname = schema.TextLine(title=u'Surname')
    age = schema.Int(title=u'Age')


class MyContent(grok.Context):
    grok.implements(IContact)
    age = 10
    surname = u"Someone"


class TestLayout(Layout):
    grok.context(interface.Interface)

    def render(self):
        return '''<!DOCTYPE HTML PUBLIC
                    "-//W3C//DTD HTML 4.01//EN"
                    "http://www.w3.org/TR/html4/strict.dtd">''' + (
                    self.view.content())
    

# Need to declare security for Zope madness
protectName(MyContent, 'age', 'zope.Public')
protectName(MyContent, 'surname', 'zope.Public')
protectName(MyContent, 'absolute_url', 'zope.Public')

# Everybody as edit right, so test are simpler
protectSetAttribute(MyContent, 'age', 'zope.Public')
protectSetAttribute(MyContent, 'surname', 'zope.Public')


class Index(view.View):
    grok.context(MyContent)

    def render(self):
        return "name: {0}; age: {1}".format(
            self.context.surname, self.context.age)


class PersonWizard(wizard.Wizard):
    grok.context(MyContent)

    def finish(self):
        print("Finish Action: {0} {1}".format(
            self.context.surname, self.context.age))
        return None


class Step1(wizard.WizardStep):
    """First form of the wizard.
    """
    wizard.view(PersonWizard)
    grok.context(MyContent)

    ignoreContent = False
    fields = Fields(IContact).select('surname')
    label = "Step Name"


class Step2(wizard.WizardStep):
    """Second form of the wizard.
    """
    wizard.view(PersonWizard)
    grok.context(MyContent)

    ignoreContent = False
    fields = Fields(IContact).select('age')
    label = "Step Age"
