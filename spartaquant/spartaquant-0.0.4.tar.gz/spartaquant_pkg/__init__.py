import importlib
import sys

modulePath = 'C:/Program Files (x86)/SpartaQuant/quantlab/api/__init__.py'
moduleName = 'sq_api'
spec = importlib.util.spec_from_file_location(moduleName, modulePath)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)

from sq_api import sq_startup