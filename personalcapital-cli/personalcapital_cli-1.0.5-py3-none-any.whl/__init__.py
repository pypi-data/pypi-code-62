# Standard Library
import json
import logging
from pathlib import Path
from typing import Any, Optional

VERSION = "1.0.5"
__version__ = VERSION
version = [1, 0, 5]

DEBT_TYPE = "Debt"
ASSET_TYPE = "Assets"

INVESTMENT_CLASS = "INVESTMENT"
BANK_CLASS = "BANK"
CREDIT_CLASS = "CREDIT_CARD"
LOAN_CLASS = "LOAN"
OTHER_CLASS = "OTHER_ASSETS"
MORTGAGE_CLASS = "MORTGAGE"

logger = logging.getLogger(__name__)


def get_file_data(filename: Optional[str], default: Any):
    """Loads and deserializes data serialized as JSON from a file."""
    if not filename:
        return default
    f = Path(filename)
    try:
        with f.open("r") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        logger.warning("%s does not exist", filename)
        return default
    except Exception:
        logger.exception("Something unexpected happened!")
        return default
    return data


def ensure_file_exists(filepath: Optional[str]):
    if not filepath:
        return
    if not Path(filepath).exists():
        raise FileNotFoundError(filepath)
