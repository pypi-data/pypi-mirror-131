"""
Working with Git Heads

Refernences:
- https://gitpython.readthedocs.io/en/stable/tutorial.html#the-tree-object
- https://gitpython.readthedocs.io/en/stable/tutorial.html#understanding-objects
"""

from git.refs.head import HEAD
from .repository import Repository


class Heads(Repository):
    """Inherits the self.repo instance"""

    def __init__(self, repo_dir='./') -> None:
        """
        Gets the repository instance inherited by super() - Default: repo_dir = './'

        Example:
        """
        super().__init__(repo_dir)

    def get_head(self) -> HEAD:
        """Return the head of the current repository"""
        return self.repo.head

    def get_heads(self) -> list:
        """Return the heads of the current repository"""
        list_heads = []
        for head in self.repo.heads:
            if head:
                list_heads.append({'heads': format(head)})

        return list_heads
