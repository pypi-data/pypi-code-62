from injecta.config.YamlConfigReader import YamlConfigReader
from injecta.container.ContainerInterface import ContainerInterface
from injecta.package.pathResolver import resolvePath
from typing import List
from pyfony.kernel.BaseKernel import BaseKernel
from pyfonybundles.Bundle import Bundle
from gitbundle.GitBundle import GitBundle

def initContainer(appEnv) -> ContainerInterface:
    class Kernel(BaseKernel):

        def _registerBundles(self) -> List[Bundle]:
            return [
                GitBundle()
            ]

    kernel = Kernel(
        appEnv,
        resolvePath('gitbundle') + '/_config',
        YamlConfigReader()
    )

    return kernel.initContainer()
