"""
Working with Git Repositories

- Checking if there are any changes
- Get a diff of changes

Refernences:
- https://gitpython.readthedocs.io/en/stable/tutorial.html#meet-the-repo-type
- https://gitpython.readthedocs.io/en/stable/tutorial.html#initializing-a-repository
"""

import sys
import git


class Repository:
    """Represents the parent (main) class of the Module"""
    def_git_repo_path = '.'

    def __init__(self, repo_dir=def_git_repo_path) -> None:
        """
        Gets the repository instance inherited by super()

        Default: repo_dir = './'

        Example:
        """
        try:
            self.repo = git.Repo(str(repo_dir))
        except git.InvalidGitRepositoryError as error:
            print(f'Oops! That was not a valid Git repository {format(error)}')
            raise
        except ValueError:
            print('That is not a string. Try again!')
            raise
        except BaseException:
            print(f'Unexpected error: {format(sys.exc_info()[0])}')
            raise

    def default_git_repo_path(self):
        """Return the hard-coded default path"""
        return self.def_git_repo_path

    def is_repo_bare(self):
        """Return True if Repository Type is Bare"""
        return bool(self.repo.bare)

    def get_description(self):
        """Return the description of the current repository"""
        return format(self.repo.description)

    def get_common_dir(self):
        """Return a list of known directories of the repository"""
        return {
            'common_dir': format(self.repo.common_dir),
            'working_tree_dir': format(self.repo.working_tree_dir),
            'working_dir': format(self.repo.working_dir),
            'git_repo_dir': format(self.repo.git_dir)
        }

    def has_separate_working_tree(self):
        """Return boolean if the repository has a separate working tree"""
        return bool(self.repo.has_separate_working_tree())

    def get_alternates(self):
        """List Alternates"""
        return list(self.repo.alternates)

    def get_cmd_wrapper_type(self):
        """Provide Git Command Wrapper Type"""
        return format(self.repo.GitCommandWrapperType)

    def get_repo_info(self):
        """Return a dictionary with all known repository information"""
        return {
            'is_bare': self.is_repo_bare(),
            'description': self.get_description(),
            'dir_list': self.get_common_dir(),
            'is_sep_worktree': self.has_separate_working_tree(),
            'alternates': self.get_alternates(),
            'cmd_wrapper': self.get_cmd_wrapper_type()
        }

    def list_remote(self) -> list:
        """Return the remote values of the current repository"""
        list_remotes = []
        for remote in self.repo.remotes:
            if remote:
                list_remotes.append(
                    {'url': format(remote.url), 'name': format(remote.name)})

        return list_remotes

    def set_new_remote_origin(self, remote_url, remote_name='origin'):
        """Create a new remote"""

        return self.repo.create_remote(remote_name, url=remote_url)

    def delete_remote(self, remote_name='origin'):
        """Delete a remote"""
        # Reference a remote by its name as part of the object
        # print(f'Remote name: {repo.remotes.origin.name}')
        # print(f'Remote URL: {repo.remotes.origin.url}')

        return self.repo.delete_remote(remote_name)

    def pull_from_remote(self):
        """Pull from remote repo"""

        return self.repo.remotes.origin.pull()

    def push_to_remote(self):
        """Push changes"""
        return self.repo.remotes.origin.push()

    # def init(self, init_repo_name):
    #     """git init new_repo"""
    #     self.init_repo_name = init_repo_name

    #     self.repo_instance.init(self.init_repo_name)

    # def clone(self, remote_repo, local_path='./'):
    #     """Clone a Repository"""
    #     self.remote_repo = remote_repo
    #     self.local_path = local_path

    #     self._clone_from_url(self.remote_repo, self.local_path )
    #     self._clone_from_local(self.remote_repo, self.local_path)

    # def _clone_from_url(self, repo_url, repo_path):
    #     """Check out via HTTPS or clone via ssh (will use default keys)"""
    #     self.repo_url = repo_url
    #     self.repo_path = repo_path

    #     self.repo_instance.clone_from(self.repo_url, self.repo_path)

    # def _clone_from_local(self, repo_path, new_path):
    #     """Load existing local repo, Create a copy of the existing repo"""
    #     self.repo_path = repo_path
    #     self.new_path = new_path

    #     local_repo = self.repo_instance(self.repo_path)
    #     local_repo.clone(self.new_path)
