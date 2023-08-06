"""
Working with Git Submodules

Refernences:
- https://gitpython.readthedocs.io/en/stable/tutorial.html#submodule-handling
"""

from typing import Any, List
from .repository import Repository


class SubModules(Repository):
    """Inherits the self.repo instance"""

    def __init__(self, repo_dir="./") -> None:
        """
        Gets the repository instance inherited by super() - Default: repo_dir = './'

        Example:
        """
        super().__init__(repo_dir)

    def get_submodules(self) -> List[Any]:
        """Return a list of submodules of the repository"""
        return list(self.repo.submodules)
