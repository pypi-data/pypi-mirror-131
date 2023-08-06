"""
Working with Git References

Refernences:
- https://gitpython.readthedocs.io/en/stable/tutorial.html#submodule-handling
"""

from .repository import Repository


class References(Repository):
    """Inherits the self.repo instance"""

    def __init__(self, repo_dir="./") -> None:
        """
        Gets the repository instance inherited by super() - Default: repo_dir = './'

        Example:
        """
        super().__init__(repo_dir)

    def get_references(self):
        """List References"""
        # return self.repo.refs
        list_refs = []
        for refs in self.repo.references:
            if refs:
                list_refs.append({
                    'commit': format(refs.commit),
                    'repo': format(refs.repo),
                    'branch': format(refs.name),
                    'object': format(refs.object),
                    'path': format(refs.path)
                })

        return list_refs
