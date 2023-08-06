"""
Working with Git Configuration

- Set git configuration values like user.email and user.name

Refernences:
-
"""

from typing import Union
from .repository import Repository


class Config(Repository):
    """Inherits the self.repo instance"""

    def __init__(self, repo_dir='./') -> None:
        """
        Gets the repository instance inherited by super() - Default: repo_dir = './'

        Example:
        """
        super().__init__(repo_dir)

    def get_config_level(self):
        """Provide the possible config level"""
        return self.repo.config_level

    def set(self, section, key, value) -> None:
        """To write configuration values, use `config_writer()`"""

        with self.repo.config_writer() as writer:
            writer.set_value(str(section), str(key), str(value))

    def get(self, section, key) -> Union[int, float, str, bool]:
        """To check configuration values, use `config_reader()`"""

        with self.repo.config_reader() as reader:
            response = reader.get_value(str(section), str(key))

        return response
