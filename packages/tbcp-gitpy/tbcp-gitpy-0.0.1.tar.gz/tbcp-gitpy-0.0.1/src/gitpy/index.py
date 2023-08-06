"""
Working with Git Index Object

Refernences:
- https://gitpython.readthedocs.io/en/stable/tutorial.html#the-index-object
- https://gitpython.readthedocs.io/en/stable/tutorial.html#understanding-objects
"""

from .repository import Repository


class Index(Repository):
    """Inherits the self.repo instance"""

    def __init__(self, repo_dir='./') -> None:
        """
        Gets the repository instance inherited by super() - Default: repo_dir = './'

        Example:
        """
        super().__init__(repo_dir)
