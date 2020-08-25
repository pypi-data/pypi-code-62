"""
  >>> from grokcore.component import testing
  >>> testing.grok(__name__)

Next we setup some content for the Wizard:

  >>> root = getRootFolder()
  >>> root['content'] = content = Content()
  >>> content
  <dolmen.forms.wizard.tests.rendering.Content ...>

Let's try to get the wizard with the help of a getMultiAdapter

  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()

  >>> from zope import component
  >>> mywizard = component.getMultiAdapter(
  ... (content, request), name='mywizard')
  >>> mywizard
  <dolmen.forms.wizard.tests.rendering.MyWizard object at ...>

Ok we can check some attributes of the Wizard. We start
with the actions:

  >>> mywizard.actions
  <Actions>
  >>> [action.title for action in mywizard.actions]
  ['Back', 'Save', 'Continue']

Do we have our steps?

  >>> mywizard.allSteps
  [<dolmen.forms.wizard.tests.rendering.Step1 object at ...>,
   <dolmen.forms.wizard.tests.rendering.Step2 object at ...>]

  >>> print(mywizard())  #doctest: +NORMALIZE_WHITESPACE
  <html>
    <body>
    <h1></h1>
    <form action="http://127.0.0.1" method="post" enctype="multipart/form-data" class="dolmen-wizard-form">
      <fieldset>
        <legend>Step1</legend>
        <div class="step-fields">
          <div class="field">
            <label class="field-label" for="form-step1-field-name">Name</label>
            <span class="field-required">*</span>
            <input type="text" value="Paul" id="form-step1-field-name" name="form.step1.field.name" class="field field-textline form-control field-required" required="required" />
          </div>
        </div>
        <div class="fields">
          <span class="field">
            <input id="form-field-step" name="form.field.step" class="field" type="hidden" value="0" />
          </span>
        </div>
        <div class="actions">
          <span class="action">
            <input type="submit" id="form-action-continue" name="form.action.continue" class="action" />
          </span>
        </div>
      </fieldset>
    </form>
    </body>
  </html>

  >>> mywizard = component.getMultiAdapter(
  ... (content, request), name='mywizard')
  >>> mywizard.step = 1
  >>> print(mywizard())  #doctest: +NORMALIZE_WHITESPACE
  <html>
    <body>
    <h1></h1>
    <form action="http://127.0.0.1" method="post" enctype="multipart/form-data" class="dolmen-wizard-form">
      <fieldset>
        <legend>Step1</legend>
        <div class="step-fields">
          <div class="field">
            <label class="field-label" for="form-step1-field-name">Name</label>
            <span class="field-required">*</span>
            <input type="text" value="Paul" id="form-step1-field-name" name="form.step1.field.name" class="field field-textline form-control field-required" required="required" />
          </div>
        </div>
        <div class="fields">
          <span class="field">
            <input id="form-field-step" name="form.field.step" class="field" type="hidden" value="0" />
          </span>
        </div>
        <div class="actions">
          <span class="action">
            <input type="submit" id="form-action-continue" name="form.action.continue" class="action" />
          </span>
        </div>
      </fieldset>
    </form>
   </body>
  </html>

"""

from zope import schema
from zope import interface
from zeam.form import composed
from zeam.form.base import Fields
from dolmen.forms import wizard
from grokcore import layout
from grokcore import component as grok


class IContact(interface.Interface):
    name = schema.TextLine(title=u'Name')
    age = schema.TextLine(title=u'Age')


class Content(grok.Context):
    name = "Paul"


class MyWizard(wizard.Wizard):
    grok.context(Content)


class Step1(wizard.WizardStep):
    composed.view(MyWizard)
    grok.context(Content)

    ignoreContent = False
    fields = Fields(IContact).select('name')
    label="Step1"


class Step2(wizard.WizardStep):
    composed.view(MyWizard)
    grok.context(Content)
    fields = Fields(IContact).select('age')
    label="Step2"


class MyLayout(layout.Layout):
    grok.context(interface.Interface)

    def render(self):
        return "<html> %s </html>" % self.view.content()
