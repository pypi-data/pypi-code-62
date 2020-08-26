from dataclasses import dataclass


@dataclass
class BaseImopayObj:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def get_fields(cls):
        return cls.__dict__.get("__annotations__", {})

    def to_dict(self):
        data = {}
        for field_name, field_type in self.get_fields().items():
            value = getattr(self, field_name)

            if self.is_empty_value(value):
                continue

            data[field_name] = field_type(value)
        return data

    @classmethod
    def from_dict(cls, data: dict):

        missing_fields = {
            field_name
            for field_name in cls.get_fields().keys()
            if field_name not in data.keys()
        }

        for missing_field in missing_fields:
            data[missing_field] = None

        return cls(**data)

    @staticmethod
    def is_empty_value(value):
        return value == "" or value is None
