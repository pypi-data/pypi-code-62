from .config_chapter import ConfigChapter


class State(ConfigChapter):
    validation_schema = {
        "type": "object",
        "required": [
            "required"
        ],
        "additionalProperties": False,
        "properties": {
            "filename": {
                "type": "string",
                "title": "State filename. Default: state.dat,.",
                "description": "State filename. Default: state.dat.",
                "maxLength": 255
            },
            "required": {
                "type": "boolean",
                "title": "Is the state used in the service? Default: false",
                "description": "Is the state used in the service? Default: false"
            },
        },
    }

    def __init__(self):
        self._state_filename = None
        self._state_required = None

    @staticmethod
    def from_yaml(input_dict):
        if input_dict is None:
            return
        state_chapter = State()
        if state_chapter.validate(input_dict, validation_schema=state_chapter.validation_schema):
            state_chapter._state_filename = input_dict.get('filename')
            state_chapter._state_required = input_dict.get('required')
            return state_chapter

    def state_filename(self):
        return self._state_filename

    def state_required(self):
        return self._state_required
