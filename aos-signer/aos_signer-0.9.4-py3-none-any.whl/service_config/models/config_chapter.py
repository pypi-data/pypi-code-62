from abc import ABC, abstractmethod

import jsonschema


class ConfigChapter(ABC):
    validation_schema = ''

    @staticmethod
    @abstractmethod
    def from_yaml(input_dict):
        pass

    @staticmethod
    def validate(received_chapter, validation_schema):
        return jsonschema.validate(received_chapter, schema=validation_schema)
