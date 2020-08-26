from io import BufferedIOBase
from hashlib import sha1
from os.path import dirname, realpath

from lxml import etree

from urllib.request import urlopen


class StableHashedString(str):
    slots = []

    def __hash__(self):
        h = sha1()
        h.update(self.encode())
        h = h.hexdigest()
        return int(h, 16)


class Param:
    slots = ["name", "types", "is_required"]

    def __init__(self, name, types, is_required, any=None):
        self.name = name
        self.types = types
        self.is_required = is_required

    def __hash__(self):
        return hash(self.name)


class ApiParser:
    __slots__ = ["primitive_types"]

    def __init__(self):
        self.primitive_types = ("Float", "Integer", "String", "Array", "Boolean")

    def extract_type_list(self, cell):
        # extract the text from the cell
        # fmt: off
        text = (cell.text or "") + "".join(
            (t if (t := elem.text) else "") +
            (t if (t := elem.tail) else "")
            for elem in cell.iterchildren()
        )
        # fmt: on

        # make "Float number" into "Float": " number" is long 7 chars
        if text[-7:] == " number":
            text = text[:-7]

        # split each type and each "Array of type"
        return [
            # fmt: off
            ((types := _type.split(" of ")).reverse() or types)
            for _type in text.split(" or ")
            # fmt: on
        ]

    def add_entity(self, _type, name, params, endpoints, types):
        if _type == 0:
            endpoints.append((name, params))
        elif _type == 1:
            types[name] = (name, params)

    def parse(self, stream: BufferedIOBase):
        # parse the HTML source
        parser = etree.HTMLParser()
        tree = etree.parse(stream, parser=parser)

        # get the version
        # actually the last div should be div[3] according to chrome, but whatever (this affects also the staritng node logic belo)
        api_version = tree.xpath("/html/body/div/div[2]/div/div/div[2]/p[1]/strong")[0].text
        api_version = api_version.rsplit(" ", 1)[1]

        # node from where to start the parsing (the getting updates section)
        starting_node = tree.xpath("/html/body/div/div[2]/div/div/div[2]/h3[4]")[0]

        # -1 is not valid, 0 is endpoint, 1 is type
        endpoints = []
        types = {}
        entity_type = -1

        # Main Type -> [Subtypes]
        aliases = {}

        # Subtype -> Main Type
        reversed_aliases = {}

        # loop variables
        name = None
        params = None

        for el in starting_node.itersiblings():
            # the telegram API page is very unfriendly to parse in some way:
            # you would expect each endpoint definition to be contained in a div or something but it's not, it's just a
            # stream of tags so we have to delimit a sequence of tags that makes sense
            if el.tag == "h4":
                # <h4> signals a new entity
                # put the current entity in the correct array, if applicable
                self.add_entity(entity_type, name, params, endpoints, types)

                # h4 tags are structured like <h4><a>link</a>ENDPOINT_NAME</a>
                name = el[0].tail
                if " " in name:
                    entity_type = -1
                    continue

                # if the name begins with a lower letter it's an endpoint, else it's a type (int(True) = 1)
                entity_type = int(name[0].isupper())

                params = []
            elif el.tag == "h3":
                # <h3> signals an end of section: append the current entity
                self.add_entity(entity_type, name, params, endpoints, types)

                # avoid appending anything else later
                entity_type = -1
            elif el.tag == "ul":
                # entities with an "ul" are lists of names that should be used instead of it
                # insert everything inside the aliases dict
                if entity_type == -1:
                    continue

                # each <li> contains an <a>
                aliases[name] = [alias[0].text for alias in el.iterchildren()]
                reversed_aliases.update((alias[0].text, name) for alias in el.iterchildren())

                # don't append the type since we have it already
                entity_type = -1
            elif el.tag == "table":
                # get the <tbody>
                table = el[1]

                # normalize the entity into an array of tuples (name, type list, required ? True : False)
                # row[0] = name
                # row[1] = type
                # row[2] =
                #   (if entity_type == 1, type) description (begins with "Optional" if optional)
                #   (if entity_type == 0, endpoint) Yes if required, Optional if optional
                params = [
                    # fmt: off
                    Param(
                        row[0].text,
                        self.extract_type_list(row[1]),
                        len(is_optional_cell := row[2]) == 0 or not is_optional_cell[0].text == "Optional"
                        if entity_type else
                        row[2].text == "Yes",
                    )
                    # fmt: on
                    for row in table.iterchildren()
                ]

        # append the last one
        self.add_entity(entity_type, name, params, endpoints, types)

        # actually used types in correct order
        used_types = []

        # get common params for each alias
        for alias, type_names in aliases.items():
            # build a set with the params of the first type
            first_type_params = types[type_names[0]][1]
            common_params = set(first_type_params)

            # keep only the intersection with each alias
            for type_name in type_names[1:]:
                params = types[type_name][1]
                common_params.intersection_update(params)

            used_types.append((alias, list(common_params)))

            # remove common params from child classes
            for type_name in type_names:
                params = types[type_name][1]
                params = set(params)
                params.difference_update(common_params)
                types[type_name] = (type_name, list(params))

        skipped_types = set(self.primitive_types)

        # begin with the types used in the endpoints (excluding primitives)
        used_type_names = set(
            StableHashedString(base_type)
            for endpoint in endpoints
            # endpoint = (name, params)
            for param in endpoint[1]
            for _type in param.types
            # _type[0] always contains either the type itself or the wrapped type (Array<T>)
            if not ((base_type := _type[0]) in skipped_types or skipped_types.add(base_type))
        )

        _used_type_names = set()
        used_types_reversed = []

        # the for loop rotates between two sets, one contains the current iteration, the other one the next
        # keep track of the types used by each type
        while True:
            for type_name in used_type_names:
                # we need to hash a normal string
                _type_name = str(type_name)

                if (type_aliases := aliases.get(_type_name, None)) :
                    # if the type has aliases we process it and add the aliases
                    _used_type_names.update(alias for alias in type_aliases)

                elif (_type := types.get(_type_name, None)) :
                    # if we have found a definition add the definition and process other custom types (if there's any)
                    used_types_reversed.append(_type)
                    _used_type_names.update(
                        StableHashedString(base_type)
                        for param in _type[1]
                        for param_type in param.types
                        if not ((base_type := param_type[0]) in skipped_types or skipped_types.add(base_type))
                    )

            if not _used_type_names:
                break

            # swap the two sets and keep iterating
            used_type_names.clear()
            used_type_names, _used_type_names = _used_type_names, used_type_names

        used_types.extend(reversed(used_types_reversed))

        return api_version, endpoints, used_types, reversed_aliases
