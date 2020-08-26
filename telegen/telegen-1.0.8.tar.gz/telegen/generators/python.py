from telegen import __version__


class PythonApiGenerator:
    __slots__ = [
        "space",
        "custom_types",
        "custom_endpoints",
        "type_to_type_map",
        "name_to_type_map",
        "name_to_value_map",
        "imports",
    ]

    def __init__(self):
        SPACE = " " * 4
        self.space = SPACE

        # types that must be implemented by hand
        self.custom_types = {
            # InputFile and related
            "InputFile",
            # ReplyMarkup
            "InlineKeyboardMarkup",
            "ReplyKeyboardMarkup",
            "ReplyKeyboardRemove",
            "ForceReply",
            # consequences of ReplyMarkup
            "KeyboardButton",
            "InlineKeyboardButton",
        }

        self.custom_endpoints = {"sendMediaGroup", "editMessageMedia"}

        # maps a Telegram APi param *type* into a Python type
        self.type_to_type_map = {
            "String": "str",
            "Integer": "int",
            "Float": "float",
            "Boolean": "bool",
        }

        # maps a Telegram API param *name* to a Python type
        self.name_to_type_map = {
            # InputFile
            "animation": "InputFile",
            "audio": "InputFile",
            "certificate": "InputFile",
            "document": "InputFile",
            "photo": "InputFile",
            "png_sticker": "InputFile",
            "sticker": "InputFile",
            "tgs_sticker": "InputFile",
            "thumb": "InputFile",
            "video": "InputFile",
            "video_note": "InputFile",
            "voice": "InputFile",
            # the media field is announced as String, good job telegram monkeys!
            "media": "InputFile",
            # other types
            "parse_mode": "ParseMode",
        }

        # maps a Telegram API param name to his value (e.g. a property on an object)
        self.name_to_value_map = {
            # InputFile
            "animation": 'animation("animation", files)',
            "audio": 'audio("audio", files)',
            "certificate": 'certificate("certificate", files)',
            "document": 'document("document", files)',
            "photo": 'photo("photo", files)',
            "png_sticker": 'png_sticker("png_sticker", files)',
            "sticker": 'sticker("sticker", files)',
            "tgs_sticker": 'tgs_sticker("tgs_sticker", files)',
            "thumb": 'thumb("thumb", files, attach="thumb")',
            "video": 'video("video", files)',
            "video_note": 'video_note("video_note", files)',
            "voice": 'voice("voice", files)',
            # other types
            "parse_mode": "parse_mode.name",
            "reply_markup": "json_dumps(reply_markup.serialized, check_circular=False)",
        }

        # added to the beginning of the generated file
        self.imports = (
            f"from json import dumps as json_dumps\n"
            f"from typing import List, Optional, Tuple, Union\n\n"
            f"try:\n"
            f"{SPACE}from typing import TypedDict\n"
            f"except:\n"
            f"{SPACE}try:\n"
            f"{SPACE}{SPACE}from mypy_extensions import TypedDict\n"
            f"{SPACE}except:\n"
            f"{SPACE}{SPACE}TypedDict = dict\n\n"
            f"from .multipart_encoder import MultipartEncoder\n"
            f"from .types import *\n\n"
            f"\n"
        )

    def build_type_definition(self, name, types):
        # if the name has a custom type we return it
        if type_def := self.name_to_type_map.get(name, None):
            return type_def

        is_union = len(types) > 1

        # else we compose the type using the definitions:
        # if the single type has length > 1 it's a List[Type]
        # e.g. for length = 3 the type is a List[List[Type]]
        # for each type use the corresponding Python type if there's one (e.g. String --> str)
        # or use the name itself if not
        return (
            # fmt: off
            ("Union[" if is_union else "") +
            ", ".join(
                "List[" * (size := len(_type) - 1) +
                self.type_to_type_map.get((base_type := _type[0]), base_type) +
                "]" * size
                for _type in types
            ) +
            ("]" if is_union else "")
            # fmt: on
        )

    def generate(self, api_version, endpoints, types, reversed_aliases):
        # avoid too much getattr machinery
        SPACE = self.space

        endpoint_defs = []
        for endpoint in endpoints:
            endpoint_name, params = endpoint

            if endpoint_name in self.custom_endpoints:
                continue

            # required params are inserted in the function declaration first
            required_params = []

            # optional params are inserted after a *, so you have to pass them with keywords
            optional_params = []

            # required params are inserted inside the dict literal when it's initialized
            params_decl = []

            # InputFiles are different for normal params and require a function call
            file_params_decl = []

            # optional params have an if guard and are inserted after the required params
            optional_params_decl = []

            # these two strings are present only if the method allows POST'ing files
            # input_file_pre initializes an array that's eventually passed to a MultipartEncoder
            # input_file_post checks if the array has been filled and returns the correct post, else falls back to the default return
            input_file_pre = ""
            input_file_post = ""

            for param in params:
                param_name = param.name
                param_types = param.types
                is_required = param.is_required
                type_def = self.build_type_definition(param_name, param_types)

                # derive the actual value from the value of the parameter
                # if the param type is not a primitive type it must be jsonified
                # fmt: off
                value = self.name_to_value_map.get(
                    param_name,
                    f"json_dumps({param_name}, check_circular=False)"
                    if param_types[0][0] not in self.type_to_type_map
                    else param_name,
                )
                # fmt: on

                # ugly special cases
                # see the descriptions in the constructor and the InputFile definition and you'll get how this works
                if type_def == "InputFile":
                    # if the method has an InputFile or InputMedia there will be some params that fill files if the media is not an url or id
                    input_file_pre = f"{SPACE}files: List[Tuple[bytes, bytes, bytes, bytes]] = []\n\n"

                    # if the media are filled we must send a POST request, else we return the usual GET
                    input_file_post = (
                        f"{SPACE}if files:\n"
                        f"{SPACE}{SPACE}headers = {{}}\n"
                        f"{SPACE}{SPACE}encoder = MultipartEncoder(files=files)\n"
                        f'{SPACE}{SPACE}headers["content-type"], body = encoder.encode()\n'
                        f'{SPACE}{SPACE}headers["content-length"] = len(body)\n'
                        f'{SPACE}{SPACE}return "POST", "{endpoint_name}", headers, params, body\n'
                        f"{SPACE}else:\n{SPACE}"
                    )

                    # the only param name that uses attach:// is thumb, for now
                    attach = '"thumb"' if param_name == "thumb" else "None"

                    if is_required:
                        required_params.append(f"{param_name}: {type_def}")
                        file_params_decl.append(
                            f'{SPACE}{param_name}("{param_name}", files, params, attach={attach})\n\n'
                        )
                    else:
                        optional_params.append(f"{param_name}: Optional[{type_def}] = None")
                        file_params_decl.append(
                            f"{SPACE}if {param_name} is not None:\n"
                            f'{SPACE}{SPACE}{param_name}("{param_name}", files, params, attach={attach})\n\n'
                        )
                else:
                    if is_required:
                        # if the type is required there's no default
                        required_params.append(f"{param_name}: {type_def}")

                        # add the param to the dict initialization
                        params_decl.append(f'{SPACE}{SPACE}"{param_name}": {value},')
                    else:
                        # if the type is optional his default value is None
                        optional_params.append(f"{param_name}: Optional[{type_def}] = None")

                        # add the param to the dict if there's no default
                        # don't format the following lines for clarity
                        # fmt: off
                        optional_params_decl.append(
                            f"{SPACE}if {param_name} is not None:\n"
                            f'{SPACE}{SPACE}params["{param_name}"] = {value}\n\n'
                        )
                        # fmt: on

            if required_params:
                # if there are required parameters we build the dict and init it with the values
                params_return_var = "params"
                # fmt: off
                params_decl = (
                    f"{SPACE}params: dict = {{\n" +
                    "\n".join(params_decl) +
                    f"\n{SPACE}}}\n\n"
                )
                # fmt: on

                # the only defference from the "only optional" case is that here we put a "," after the required params
                # and before the optional params (if there are any)
                required_params = f"\n{SPACE}" + f",\n{SPACE}".join(required_params)
                optional_params = (
                    (f",\n{SPACE}*,\n{SPACE}" + f",\n{SPACE}".join(optional_params) + "\n") if optional_params else "\n"
                )

            elif optional_params:
                # if there are only optional parameters we create the dict but return None if the dict is not good
                params_return_var = "params"
                params_decl = f"{SPACE}params: dict = {{}}\n\n"

                required_params = ""
                optional_params = f"*,\n{SPACE}" + f",\n{SPACE}".join(optional_params) + "\n"
            else:
                # if there are no params we return None and don't even create the dict
                params_return_var = "None"
                params_decl = ""
                required_params = ""
                optional_params = ""

            file_params_decl = "".join(file_params_decl)
            optional_params_decl = "".join(optional_params_decl)

            endpoint_defs.append(
                f"def {endpoint_name}({required_params}{optional_params}) -> EndpointCall:\n"
                f"{input_file_pre}"
                f"{params_decl}"
                f"{file_params_decl}"
                f"{optional_params_decl}"
                f"{input_file_post}"
                f'{SPACE}return "GET", "{endpoint_name}", None, {params_return_var}, None\n\n\n'
            )

        type_defs = []
        for _type in types:
            type_name, params = _type

            if type_name in self.custom_types:
                continue

            required_params = []
            optional_params = []

            for param in params:
                param_name = param.name
                param_types = param.types
                type_def = self.build_type_definition(param_name, param_types)

                if param.is_required:
                    required_params.append(f"{SPACE}{param_name}: {type_def}")
                else:
                    optional_params.append(f"{SPACE}{param_name}: Optional[{type_def}]")

            if required_params:
                required_params = "\n".join(required_params)
                optional_params = ("\n" + "\n".join(optional_params)) if optional_params else ""
            else:
                required_params = ""
                optional_params = "\n".join(optional_params) if optional_params else f"{SPACE}pass"

            base_class = reversed_aliases.get(type_name, "TypedDict")

            # fmt: off
            type_defs.append(
                f"class {type_name}({base_class}, total=False):\n"
                f"{required_params}"
                f"{optional_params}\n\n\n"
            )
            # fmt: on

        code = self.imports + "".join(type_defs) + "".join(endpoint_defs)

        return [("telegen_definitions/generated.py", code), ("version.txt", f"{api_version}.{__version__}")]
