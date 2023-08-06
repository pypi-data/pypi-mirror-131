"""
Working with Git Tree Object

Refernences:
- https://gitpython.readthedocs.io/en/stable/tutorial.html#the-tree-object
- https://gitpython.readthedocs.io/en/stable/tutorial.html#understanding-objects
"""

from .repository import Repository


class Tree(Repository):
    """Inherits the self.repo instance"""

    def __init__(self, repo_dir='./') -> None:
        """
        Gets the repository instance inherited by super() - Default: repo_dir = './'

        Example:
        """
        super().__init__(repo_dir)

    def get_trees(self):
        """Provide a list of all Trees of the given Branch Tree"""
        tree_main = self.repo.heads.main.commit.tree

        list_trees = []
        for tree_trees in tree_main.trees:
            if tree_trees:
                list_trees.append(format(tree_trees))

        return list_trees

    def get_blobs(self):
        """Provide a list of all Blobs of the given Branch Tree"""
        tree_main = self.repo.heads.main.commit.tree

        list_blobs = []
        for tree_blobs in tree_main.blobs:
            if tree_blobs:
                list_blobs.append(format(tree_blobs))

        return list_blobs
