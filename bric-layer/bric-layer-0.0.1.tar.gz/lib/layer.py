import docker
from dis import dis
from munch import Munch

from lib.load_config import Config
from lib.logger import initialize_logger
from lib.framer import Framer
from lib.bric_builder.bric_builder import BricBuilder
from lib.plugs.plug_loader import Plugs

# declare app modules
# you can use the app in modules before initializing them, by converting the module to be initialized as a function
# and passing the self object to the module
'''IMPORTANT! The order in which modules are added to the app is crucial to the proper build of the app.'''


class Layer:
    def __init__(self, env=None):
        # TODO - wrap all functions in dis when calling in dev mode
        self.dis = dis

        # set config level
        self.config = Munch.fromDict(Config(env))

        # TODO - change logging based on environment
        # set log level
        self.log = initialize_logger()

        # set pandas with config and extensions
        self.framer = Framer(self)

        # TODO - config plugs
        self.plugs = Plugs(self)

        # TODO - create 'brics' directory with 'main.py' if they do not exist
        # set bric_builder config
        self.bric_builder = BricBuilder(self)

        # all brics
        self.brics = {}

        # current bric
        self.current = {}

    # TODO - config docker builder factory
    # set docker_builder
    docker_builder = docker

    def mold_brics(self, bric_list='all'):
        self.brics = self.bric_builder.mold_brics(bric_list)

    # TODO - the code below works with only one bric for now, do not execute multiple brics
    #  until they are separate microservices
    def lay_bric(self, bric_name):
        self.current = self.brics[bric_name]
        self.current.config = self.config.load_bric_config(bric_name)
        build_bric = self.current.Main(self)
        build_bric.assemble()

    def lay_brics(self):
        for module in self.brics:
            self.lay_bric(module)

    # TODO - execute in parallel
    def lay_brics_parallel(self):
        self.lay_brics()

