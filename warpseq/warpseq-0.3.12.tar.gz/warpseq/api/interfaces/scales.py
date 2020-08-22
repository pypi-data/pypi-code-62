# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.model.note import Note
from warpseq.model.scale import Scale, scale_types
from warpseq.api.interfaces.base import CollectionApi

class Scales(CollectionApi):

    object_class    = Scale
    public_fields   = [ 'name', 'scale_type', 'slots' ] # this is somewhat ignored because of the methods below
    song_collection = 'scales'
    add_method      = 'add_scales'
    add_required    = [ ]
    edit_required   = [ ]
    remove_method   = 'remove_track'
    nullable_edits  = [ 'scale_type', 'slots', 'note', 'octave' ]

    def _check_params(self, params, for_edit=False):
        slots = params['slots']
        root = self._get_note(params)
        params['root'] = root
        scale_type = params['scale_type']
        if scale_type is None and slots is None:
            if not for_edit:
                raise InvalidInput("either scale_type or slots is required")
        if slots is not None and scale_type is not None:
            raise InvalidInput("scale_type and slots are mutually exclusive")
        del params['note']
        del params['octave']

    def _get_note(self, params):
        note = params['note']
        octave = params['octave']
        if note and (octave is not None):
            return Note(name=note, octave=octave)
        else:
            return None

    def _update_details(self, details, obj):
        if obj.root:
            details['note'] = obj.root.name
            details['octave'] = obj.root.octave
        else:
            details['note'] = None
            details['octave'] = None

    def add(self, name, note:str=None, octave:int=None, scale_type:str=None, slots:list=None):
        params = locals()
        self._check_params(params)
        return self._generic_add(name, params)

    def edit(self, name, new_name:str=None, note:str=None, octave:int=None, scale_type:str=None, slots:list=None):
        params = locals()
        self._check_params(params, for_edit=True)
        return self._generic_edit(name, params)

    def scale_types(self):
        return scale_types()