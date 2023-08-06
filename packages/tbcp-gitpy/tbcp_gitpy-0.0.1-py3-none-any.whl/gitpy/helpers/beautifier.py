"""Provide function to work with Commit objects"""


def commit_beautifier(commit_instance):
    """Convert given Commit Instance in structered Object"""
    object_commit = {
        'hexsha': str(commit_instance.hexsha),
        'tree': {
            'type': str(commit_instance.tree.type)
        },
        'summary': format(commit_instance.summary),
        'message': format(commit_instance.message),
        'parents': commit_instance.parents,
        'author': {
            'name': str(commit_instance.author.name),
            'email': str(commit_instance.author.email)
        },
        'committer': {
            'name': str(commit_instance.committer.name),
            'email': str(commit_instance.committer.email),
        },
        'authored_datetime': format(commit_instance.authored_datetime),
        'authored_date': int(commit_instance.authored_date),
        'committed_date': int(commit_instance.committed_date),
        'count': int(commit_instance.count()),
        'size': int(commit_instance.size)
    }
    return object_commit
