"""
Working with Git Commits object

Reference:
- https://gitpython.readthedocs.io/en/stable/tutorial.html#the-commit-object
- https://gitpython.readthedocs.io/en/stable/tutorial.html#understanding-objects
"""

from .repository import Repository
from .helpers import commit_beautifier


class Commits(Repository):
    """Inherits the self.repo instance"""

    def __init__(self, repo_dir='./') -> None:
        """
        Gets the repository instance inherited by super() - Default: repo_dir = './'

        Example:
        """
        super().__init__(repo_dir)

    def get_recent(self) -> object:
        """Return the latest commit of the repository"""
        return commit_beautifier(self.repo.head.commit)

    def list_commits(self, max_count=50, skip=0, head="main") -> list:
        """
        Provide a list of commits. Default: max=50, head=main, skip=0

        - commit.hexsha
        - commit.summary
        - commit.author.name
        - commit.author.email
        - commit.authored_datetime
        - commit.count()
        - commit.size
        """

        list_commits = []
        for commit in list(self.repo.iter_commits(head, max_count=max_count, skip=skip)):
            if commit:
                list_commits.append(commit_beautifier(commit))

        return list_commits

    def get_data_by_hexsha(self, hexsha: str, head="main"):
        """
        Provide a list of commits. Default: max=50, head=main, skip=0

        - commit.hexsha
        - commit.summary
        - commit.author.name
        - commit.author.email
        - commit.authored_datetime
        - commit.count()
        - commit.size
        """

        commit_data = {}
        for commit in list(self.repo.iter_commits(head)):
            if commit.hexsha == hexsha:
                commit_data = commit_beautifier(commit)

        return commit_data

# headcommit = repo.head.commit
# assert len(headcommit.hexsha) == 40
# assert len(headcommit.parents) > 0
# assert headcommit.tree.type == 'tree'
# assert len(headcommit.author.name) != 0
# assert isinstance(headcommit.authored_date, int)
# assert len(headcommit.committer.name) != 0
# assert isinstance(headcommit.committed_date, int)
# assert headcommit.message != ''

#     def catch_commit_from_hook(self, repo_instance):
#         """Catch a commit message"""
#         self.repo_instance = repo_instance

#         self.repo_instance.index.commit('Initial commit.')

#     def take_commit_message(self, repo_instance, commit_message):
#         """Provide a commit message"""
#         self.repo_instance = repo_instance
#         self.commit_message = commit_message

#         self.repo_instance.index.commit('Initial commit.')
