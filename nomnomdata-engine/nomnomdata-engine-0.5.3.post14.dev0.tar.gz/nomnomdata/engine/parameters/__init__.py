import datetime
from dataclasses import dataclass
from enum import Enum as pyEnum
from logging import getLogger
from typing import List

from nomnomdata.engine.components import ParameterType
from nomnomdata.engine.errors import ValidationError

__all__ = [
    "Boolean",
    "Code",
    "CodeDialectType",
    "Date",
    "DateTime",
    "Enum",
    "EnumDisplayType",
    "EnumList",
    "Int",
    "MetaDataTable",
    "String",
    "Text",
]

_logger = getLogger("nomigen.parameters")


class CodeDialectType(str, pyEnum):
    ABAP = "abap"
    ABC = "abc"
    ACTIONSCRIPT = "actionscript"
    ADA = "ada"
    APACHE_CONF = "apache_conf"
    APEX = "apex"
    APPLESCRIPT = "applescript"
    ASCIIDOC = "asciidoc"
    ASL = "asl"
    ASSEMBLY_X86 = "assembly_x86"
    AUTOHOTKEY = "autohotkey"
    BATCHFILE = "batchfile"
    BRO = "bro"
    C_CPP = "c_cpp"
    C9SEARCH = "c9search"
    CIRRU = "cirru"
    CLOJURE = "clojure"
    COBOL = "cobol"
    COFFEE = "coffee"
    COLDFUSION = "coldfusion"
    CSHARP = "csharp"
    CSOUND_DOCUMENT = "csound_document"
    CSOUND_ORCHESTRA = "csound_orchestra"
    CSOUND_SCORE = "csound_score"
    CSP = "csp"
    CSS = "css"
    CURLY = "curly"
    D = "d"
    DART = "dart"
    DIFF = "diff"
    DJANGO = "django"
    DOCKERFILE = "dockerfile"
    DOT = "dot"
    DROOLS = "drools"
    EDIFACT = "edifact"
    EIFFEL = "eiffel"
    EJS = "ejs"
    ELIXIR = "elixir"
    ELM = "elm"
    ERLANG = "erlang"
    FORTH = "forth"
    FORTRAN = "fortran"
    FSHARP = "fsharp"
    FSL = "fsl"
    FTL = "ftl"
    GCODE = "gcode"
    GHERKIN = "gherkin"
    GITIGNORE = "gitignore"
    GLSL = "glsl"
    GOBSTONES = "gobstones"
    GOLANG = "golang"
    GRAPHQLSCHEMA = "graphqlschema"
    GROOVY = "groovy"
    HAML = "haml"
    HANDLEBARS = "handlebars"
    HASKELL = "haskell"
    HASKELL_CABAL = "haskell_cabal"
    HAXE = "haxe"
    HJSON = "hjson"
    HTML = "html"
    HTML_ELIXIR = "html_elixir"
    HTML_RUBY = "html_ruby"
    INI = "ini"
    IO = "io"
    JACK = "jack"
    JADE = "jade"
    JAVA = "java"
    JAVASCRIPT = "javascript"
    JSON = "json"
    JSONIQ = "jsoniq"
    JSP = "jsp"
    JSSM = "jssm"
    JSX = "jsx"
    JULIA = "julia"
    KOTLIN = "kotlin"
    LATEX = "latex"
    LESS = "less"
    LIQUID = "liquid"
    LISP = "lisp"
    LIVESCRIPT = "livescript"
    LOGIQL = "logiql"
    LOGTALK = "logtalk"
    LSL = "lsl"
    LUA = "lua"
    LUAPAGE = "luapage"
    LUCENE = "lucene"
    MAKEFILE = "makefile"
    MARKDOWN = "markdown"
    MASK = "mask"
    MATLAB = "matlab"
    MAZE = "maze"
    MEL = "mel"
    MIXAL = "mixal"
    MUSHCODE = "mushcode"
    MYSQL = "mysql"
    NIX = "nix"
    NSIS = "nsis"
    OBJECTIVEC = "objectivec"
    OCAML = "ocaml"
    PASCAL = "pascal"
    PERL = "perl"
    PERL6 = "perl6"
    PGSQL = "pgsql"
    PHP = "php"
    PHP_LARAVEL_BLADE = "php_laravel_blade"
    PIG = "pig"
    PLAIN_TEXT = "plain_text"
    POWERSHELL = "powershell"
    PRAAT = "praat"
    PROLOG = "prolog"
    PROPERTIES = "properties"
    PROTOBUF = "protobuf"
    PUPPET = "puppet"
    PYTHON = "python"
    R = "r"
    RAZOR = "razor"
    RDOC = "rdoc"
    RED = "red"
    REDSHIFT = "redshift"
    RHTML = "rhtml"
    RST = "rst"
    RUBY = "ruby"
    RUST = "rust"
    SASS = "sass"
    SCAD = "scad"
    SCALA = "scala"
    SCHEME = "scheme"
    SCSS = "scss"
    SH = "sh"
    SJS = "sjs"
    SLIM = "slim"
    SMARTY = "smarty"
    SNIPPETS = "snippets"
    SOY_TEMPLATE = "soy_template"
    SPACE = "space"
    SPARQL = "sparql"
    SQL = "sql"
    SQLSERVER = "sqlserver"
    STYLUS = "stylus"
    SVG = "svg"
    SWIFT = "swift"
    TCL = "tcl"
    TERRAFORM = "terraform"
    TEX = "tex"
    TEXT = "text"
    TEXTILE = "textile"
    TOML = "toml"
    TSX = "tsx"
    TURTLE = "turtle"
    TWIG = "twig"
    TYPESCRIPT = "typescript"
    VALA = "vala"
    VBSCRIPT = "vbscript"
    VELOCITY = "velocity"
    VERILOG = "verilog"
    VHDL = "vhdl"
    VISUALFORCE = "visualforce"
    WOLLOK = "wollok"
    XML = "xml"
    XQUERY = "xquery"
    YAML = "yaml"

    def __str__(self):
        return self.value


@dataclass
class MetaDataTable(ParameterType):
    type = "metadata_table"


@dataclass
class Boolean(ParameterType):
    """
        A boolean switch

        :rtype: bool
    """

    type = "boolean"
    default: bool = None


@dataclass
class Int(ParameterType):
    """
        One line integer input box.

        :rtype: int
    """

    type = "int"
    shared_object_type_uuid = "INT-SHAREDOBJECT"
    default: int = None
    max: int = None
    min: int = None

    def validate(self, val):
        if not isinstance(val, int):
            raise ValidationError(f"{type(val)} is not expected Integer type")
        if self.min and val < self.min:
            raise ValidationError(f"{val} is smaller than specified minimum [{self.min}]")
        if self.max and val > self.max:
            raise ValidationError(f"{val} is larger than specified maximum [{self.max}]")
        return True


@dataclass
class String(ParameterType):
    """
        Single line string input box.

        :rtype: bool
    """

    type = "string"
    default: str = None
    shared_object_type_uuid = "STRING-SHAREDOBJECT"
    max: int = None
    min: int = None

    def validate(self, val):
        if not isinstance(val, str):
            raise ValidationError(f"{type(val)} is not expected String type")
        if self.min and len(val) < self.min:
            raise ValidationError(
                f"{val} is smaller than specified minimum length [{self.min}]"
            )
        if self.max and len(val) > self.max:
            raise ValidationError(
                f"{val} is larger than specified maximum length [{self.max}]"
            )
        return True


@dataclass
class Code(String):
    """
        Text box with syntax validation
        and highlighting. Valid syntax is defined by
        the :class:`~nomnomdata.engine.parameters.CodeDialectType` you pass in

        :rtype: str
    """

    shared_object_type_uuid = None

    type = "code"
    dialect: CodeDialectType = CodeDialectType.JSON
    default: str = None


@dataclass
class Text(String):
    """
        Expandable text box

        :rtype: str
    """

    shared_object_type_uuid = None

    type = "text"
    default: str = None


@dataclass
class Enum(ParameterType):
    """
        Dropdown selection box.

        :rtype: bool
    """

    type = "enum"
    choices: List[str]
    default: str = None

    def _ensure_type(self, val):
        if not isinstance(val, str):
            raise TypeError(f"{type(val)} is not a string")

    def load(self, val):
        self._ensure_type(val)
        return val

    def dump(self, val):
        self._ensure_type(val)
        return val

    def validate(self, val):
        if val not in self.choices:
            raise ValidationError(f"{val} is not a valid choice")
        return True


class EnumDisplayType(str, pyEnum):
    checkbox_group = "checkbox_group"
    tag_select = "tag_select"


@dataclass
class EnumList(ParameterType):
    """
        Either a group of checkboxes, or a tag list with a dropdown selection + autocomplete style search.
        Multiple visual representations can be selected by passing :class:`~nomnomdata.engine.parameters.EnumDisplayType`

        :rtype: bool
    """

    type = "enum_list"
    choices: List[str]
    display_type: EnumDisplayType
    default: List[str] = None

    def _ensure_types(self, val):
        if not isinstance(val, list):
            raise TypeError(f"{type(val)} is not a list, expecting List[str]")
        for sub_val in val:
            if not isinstance(sub_val, str):
                raise TypeError(f"{type(sub_val)} is not a str, expecting List[str]")

    def load(self, val: List[str]):
        self._ensure_types(val)
        return val

    def dump(self, val):
        self._ensure_types(val)
        return val

    def validate(self, val: List[str]):
        for sub_val in val:
            if sub_val not in self.choices:
                raise ValidationError(
                    f"{sub_val} is not a valid choice, available choices are {self.choices}"
                )
        return True


@dataclass
class Date(ParameterType):
    """
        Will be represented by a date picker in the UI

        :rtype: datetime.date
    """

    type = "date"
    default: datetime.date = None

    def dump(self, val: datetime.date):
        return val.isoformat()

    def load(self, val: str):
        return datetime.date.fromisoformat(val)


@dataclass
class DateTime(ParameterType):
    """
        Will be represented by a date picker in the UI

        :rtype: datetime.date
    """

    type = "date"
    default: datetime.datetime = None

    def dump(self, val: datetime.datetime):
        if val.tzinfo is not None and val.tzinfo.utcoffset(val) is not None:
            return val.isoformat()
        else:
            raise ValueError("Datetime must be timezone aware")

    def load(self, val: str):
        result = datetime.datetime.fromisoformat(val)
        if result.tzinfo is not None and result.tzinfo.utcoffset(result) is not None:
            return result
        else:
            raise ValueError(f"Unable to parse timezone offset information from {val}")
