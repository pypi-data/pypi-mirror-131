"""
Working with Git Branches

- Listing branches
- Creating branches
- Switching branches

Refernences:
- https://gitpython.readthedocs.io/en/stable/tutorial.html#switching-branches
"""

from .repository import Repository


class Branches(Repository):
    """Inherits the self.repo instance"""

    def __init__(self, repo_dir="./") -> None:
        """
        Gets the repository instance inherited by super() - Default: repo_dir = './'

        Example:
        """
        super().__init__(repo_dir)

    def get_branch(self):
        """Return the active branch of the current repository"""
        return format(self.repo.active_branch)

    def list_branches(self):
        """List all branches of the local repository"""

        list_branches = []
        for branch in self.repo.branches:
            if branch:
                list_branches.append(format(branch))

        return list_branches

    def check_if_branch_exists(self, branch) -> bool:
        """Check if the given branch exists"""

        return bool(branch in self.list_branches())

    def create_branch(self, branch_name: str, checkout=True, from_branch='main'):
        """Return the active branch of the current repository"""

        if self.check_if_branch_exists(branch_name):
            head = self.repo.create_head(branch_name)

            if checkout:
                head.checkout()

            if from_branch == 'main':
                pull_branch = self.repo.heads.main
            else:
                pull_branch = self.repo.heads[from_branch]

            self.repo.git.pull('origin', pull_branch)

        if self.repo.index.diff(None) or self.repo.untracked_files:

            self.repo.git.add(A=True)
            self.repo.git.commit(m='msg')
            self.repo.git.push('--set-upstream', 'origin', head)
