"""
Working with Git Files

- Add and commit files

Refernences:
- https://gitpython.readthedocs.io/en/stable/tutorial.html#obtaining-diff-information
"""

from .repository import Repository


class Files(Repository):
    """Inherits the self.repo instance"""

    def __init__(self, repo_dir='./') -> None:
        """
        Gets the repository instance inherited by super() - Default: repo_dir = './'

        Example:
        """
        super().__init__(repo_dir)

    def has_changes(self) -> bool:
        """Return True if the repository has changed files (untracked files)"""
        return bool(self.repo.is_dirty(untracked_files=True))

    def list_untracked_files(self) -> list:
        """Provide a list of the files to stage"""
        return list(self.repo.untracked_files)

    def get_diff(self):
        """Return the difference since the last commit"""
        return self.repo.git.diff(self.repo.head.commit.tree)
