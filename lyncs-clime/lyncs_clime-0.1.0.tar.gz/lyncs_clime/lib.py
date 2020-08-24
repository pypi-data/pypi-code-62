"Loads the c-lime library"

__all__ = [
    "lib",
    "PATHS",
]

from lyncs_cppyy import Lib
from . import __path__

PATHS = list(__path__)

lib = Lib(
    path=PATHS,
    header="lime.h",
    library="liblime.so",
    c_include=True,
    check="LimeRecordHeader",
)
