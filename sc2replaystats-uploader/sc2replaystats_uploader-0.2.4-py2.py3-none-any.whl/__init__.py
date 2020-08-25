"""Top-level package for sc2replaystats_uploader."""

__author__ = """Dominik Stańczak"""
__email__ = "stanczakdominik@gmail.com"

from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
     # package is not installed
    pass
