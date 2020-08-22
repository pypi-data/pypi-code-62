# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

import importlib

def _make_reference(obj):
    return dict(
        _ID=obj.obj_id,
        _TYP=k
    )

def save_object(obj):

    from warpseq.model.base import NewReferenceObject

    if obj is None:
        return None
    if type(obj) in [ int, float, bool, str ]:
        return obj
    if type(obj) == list:
        return [ save_object(x) for x in obj]
    elif type(obj) == dict:
        return { x : save_object(y) for (x,y) in obj.items() }

    reference_hints = obj.__class__.SAVE_AS_REFERENCES

    results = dict()
    results["_CLS"] = (obj.__class__.__module__, obj.__class__.__name__, )

    for k in obj.__slots__:
        value = getattr(obj, k)
        if k.startswith("_"):
            continue
        if value is None:
            results[k] = None
        elif isinstance(value, object):
            # objects that are top level members of Song referenced in lower-level objects on the tree
            # must be saved as references
            if k in reference_hints and isinstance(value, NewReferenceObject):
                results[k] = dict(_ID=value.obj_id, _TYP=k)
            else:
                results[k] = save_object(value)
        else:
            results[k] = save_object(value)

    return results

# ------------------------------------------------------------------------------------

def load_object(song, data):

    if data is None:
        return None

    if type(data) in [ int, float, bool, str ]:
        return data

    if type(data) == list:
        return [ load_object(song, x) for x in data ]

    if '_ID' in data:
        method = getattr(song, "find_%s" % data['_TYP'])
        return method(data['_ID'])

    if '_CLS' in data:
        (mod, classname) = data['_CLS']
        mod = importlib.import_module(mod)
        cls = getattr(mod, classname)
        del data['_CLS']
        params = { x : load_object(song, y) for (x,y) in data.items() }
        return cls(**params)

    return { k : load_object(song, v) for (k, v) in data.items() }
