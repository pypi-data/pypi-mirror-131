"""Working with Git Git Tags."""

from .repository import Repository


class Tags(Repository):
    """Inherits the self.repo instance."""

    def __init__(self, repo_dir: str) -> None:
        """Get the repository instance inherited by super().

        Default: repo_dir = './'
        """
        super().__init__(repo_dir)

    def get_tags(self) -> list:
        """Return the tags of the current repository."""
        list_tags = []
        for tag in self.repo.tags:
            if tag:
                list_tags.append({'tag': tag.tag, 'commit': tag.commit})

        return list(list_tags)

    def get_tags_info(self) -> dict:
        """Return a dictionary with all known repository information."""
        return {
            'tags': self.get_tags()
        }

    def create_tag(self, tag_name: str, tag_message: str) -> None:
        """Create new Tag."""
        self.repo.create_tag(tag_name, message=tag_message)

    def delete_tag(self, tag_index: str) -> None:
        """Delete Tag."""
        tags = self.repo.tags
        tagref = tags[tag_index]  # Search for Tag Index

        self.repo.delete_tag(tagref)
