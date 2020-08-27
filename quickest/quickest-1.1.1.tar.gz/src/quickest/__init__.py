__version__ = '0.1.0'

from .core.api import StoppingProblem
from .app.io import get_logger, load_config
from .app.cli import list_menu, input_prompt


app_name='quickest'