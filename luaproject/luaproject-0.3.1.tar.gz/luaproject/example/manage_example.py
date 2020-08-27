import os
from luaproject import LuaProjectManager
import example

application_root = os.path.abspath(os.path.dirname(example.__file__))
manager = LuaProjectManager(application_root).get_manager()

if __name__ == "__main__":
    manager()