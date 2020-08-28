from .models import *
import autocomplete_light.shortcuts as autocomplete_light
from django.db.models import Q

autocomplete_light.register(Cliente,
                name='ClienteManyAutocomplete',
                search_fields=('nombre',),
                choices= Cliente.objects.all(),
                autocomplete_js_attributes={ 'placeholder': 'Busca un cliente... ', },
                widget_js_attributes = {
                                        'max_values': 20,
                                        }
                )