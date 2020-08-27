import re
from pathlib import Path
from pyfonybundles.Bundle import Bundle
from gitbundle.branch.CurrentBranchResolver import CurrentBranchResolver
from gitbundle.repository.CurrentRepositoryFactory import CurrentRepositoryFactory

class GitBundle(Bundle):

    def __init__(self, basePath: Path = Path.cwd()):
        self._currentBranchResolver = CurrentBranchResolver(CurrentRepositoryFactory(basePath))

    def getConfigFiles(self):
        return []

    def modifyRawConfig(self, rawConfig: dict) -> dict:
        if 'parameters' not in rawConfig:
            return rawConfig

        currentBranch = self._currentBranchResolver.resolve()

        rawConfig['parameters']['gitbundle'] = dict(
            currentBranch=currentBranch,
            currentBranchWithoutFeature=re.sub(r'^feature/', '', currentBranch)
        )

        return rawConfig
