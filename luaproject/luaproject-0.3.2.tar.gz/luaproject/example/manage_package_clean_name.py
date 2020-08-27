import os
from luaproject import LuaProjectManager
import package_clean_name

application_root = os.path.abspath(os.path.dirname(package_clean_name.__file__))
manager = LuaProjectManager(application_root).get_manager()

if __name__ == "__main__":
    manager()
