import re
from _pygit2 import GitError # pylint: disable = no-name-in-module
from gitbundle.repository.CurrentRepositoryFactory import CurrentRepositoryFactory

class CurrentBranchResolver:

    def __init__(
        self,
        currentRepositoryFactory: CurrentRepositoryFactory,
    ):
        self.__currentRepositoryFactory = currentRepositoryFactory

    def resolve(self) -> str:
        try:
            return self.__currentRepositoryFactory.create().head.shorthand
        except GitError as e:
            matches = re.match(r"^reference 'refs/heads/([^']+)' not found$", str(e))

            # No commit found in current branch yet -> only master branch can exists
            if matches:
                return matches.groups()[0]

            raise
