def empty_schema_field_dict(schema_dict):
    """Return the schema fields as a typical dict (that you would normally interact with) with all fields empty"""
    return {field['name']: '' if isinstance(field['type'], str) else empty_schema_field_dict(field['type'])
            for field in schema_dict['fields']}
