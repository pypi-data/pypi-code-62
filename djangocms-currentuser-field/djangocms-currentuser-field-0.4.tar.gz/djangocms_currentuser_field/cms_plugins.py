from aldryn_forms.cms_plugins import Field
from aldryn_forms.forms import ExtandableErrorForm
from cms.plugin_pool import plugin_pool
from django import forms
from django.utils.translation import ugettext as _
from django.conf import settings

from .models import CurrentUserFieldPlugin


class CurrentUserFieldForm(ExtandableErrorForm):
    class Meta:
        fields = ['label', 'name', 'initial_value', 'custom_classes']


@plugin_pool.register_plugin
class CurrentUserField(Field):
    """
    Field to be used with aldryn-forms, stores the current logged in user in.
    We use the initial_value field to store which value the user wants to save.
    """
    name = _('Current User Field')
    form = CurrentUserFieldForm
    form_field_widget_input_type = 'text'
    model = CurrentUserFieldPlugin
    fieldset_general_fields = ['label', 'name', 'initial_value', 'custom_classes']
    fieldset_advanced_fields = []
    form_field = forms.CharField
    form_field_widget = forms.CharField.widget
    form_field_enabled_options = [
            'label',
            'name',
            'initial_value',
        ]
    fieldset_advanced_fields = [
        'attributes',
    ]

    def get_form_field(self, instance):
        """
        Customize the form field
        """
        field = super(CurrentUserField, self).get_form_field(instance)

        field.required = False
        field.disabled = True   # Don't let the user edit

        return field


    def get_value(self, request, instance):
        """
        Returns the field value based on what the user specified
        they want the field to contain (initial_value).
        """
        if not hasattr(request, 'user'):
            return ""
        
        user = request.user
        
        if instance.initial_value == 'username':
            try:
                return user.username
            except AttributeError:
                return None

        elif instance.initial_value == 'email':
            try:
               return user.email
            except AttributeError:
                return None

        elif instance.initial_value == 'userid':
            try:
                # If we have a user class override set, use that
                # for the user id
                use_subclass = settings.CURRENTUSER_FIELD_USER_SUBCLASS
                if use_subclass and hasattr(user, use_subclass):
                    return getattr(user, use_subclass).id
            except AttributeError:
                pass

            # Otherwise, it's the regular user id
            return user.id

        elif instance.initial_value == 'firstlast':
            try:
                return ' '.join([user.first_name, user.last_name])
            except AttributeError:
                return None

        elif instance.initial_value == 'lastfirst':
            try:
                return ', '.join([user.last_name, user.first_name])
            except AttributeError:
                return None
        
        else:   # a custom field
            try:
                return getattr(user, instance.initial_value)
            except AttributeError:
                pass

            try:
                user_subclass = getattr(user, settings.CURRENTUSER_FIELD_USER_SUBCLASS)
                return getattr(user_subclass, instance.initial_value)
            except AttributeError:
                pass

        return None


    def render(self, context, instance, placeholder):
        """
        Replace the initial field value with the current logged in username
        before we render the field.
        """
        form = context.get('form')
        if not form:
            return context
        
        field_name = form.form_plugin.get_form_field_name(field=instance)
        form.fields[field_name].initial = self.get_value(context['request'], instance)

        context = super(CurrentUserField, self).render(context, instance, placeholder)
        return context


    def form_pre_save(self, instance, form, **kwargs):
        """
        Set the field value (don't use the user input)
        """
        request = kwargs['request']
        field_name = form.form_plugin.get_form_field_name(field=instance)
        form.cleaned_data[field_name] = self.get_value(request, instance)
