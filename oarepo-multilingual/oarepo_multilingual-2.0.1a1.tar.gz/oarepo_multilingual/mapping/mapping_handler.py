# -*- coding: utf-8 -*- #
"""Simple test of version import."""
def handler(type=None, resource=None, id=None, json_pointer=None,
            app=None, content=None, root=None, content_pointer=None):
    """Use this function as handler."""
    languages = app.config.get("SUPPORTED_LANGUAGES", [])
    data_dict= dict()

    for x in languages:
        data_dict[x] = {"type" : "text",
                                               'fields': {
                                                   "keywords":{
                                                       "type": "keyword"
                                                   }
                                               }
                                         }

    return {
        "type": "object",
        "properties": data_dict
    }
