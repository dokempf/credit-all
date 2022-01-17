"""Utilities to locate relevant files on the filesystem """

import git
import jinja2
import json
import os


def is_in_git_repository():
    """Whether or not the current working directory resides in a git repository"""
    try:
        git.Repo(os.getcwd(), search_parent_directories=True)
        return True
    except git.InvalidGitRepositoryError:
        return False


def get_repository():
    """Find the root of the git repository of the working directory

    This assumes that the working directory *is* part of a git repository.
    """
    repo = git.Repo(os.getcwd(), search_parent_directories=True)
    return repo.git.rev_parse("--show-toplevel")


def allcontributorsrc_path_list():
    """Create a list of paths to look for .all-contributorsrc"""

    path_list = [os.getcwd()]

    if is_in_git_repository():
        path_list.append(get_repository())

    return path_list


def rolefile_path_list():
    """Create a list of paths to look for role definition files"""

    # We reuse above list for the all-contributorsrc file
    path_list = allcontributorsrc_path_list()

    # And extend it with the package installation directory
    path, _ = os.path.split(__file__)
    path_list.append(path)

    return path_list


def find_file_in_path_list(filename, path_list):
    # Iterate through the given paths to find the file
    for path in path_list:
        full_path = os.path.join(path, filename)
        if os.path.exists(full_path):
            return full_path

    # If we did not find one, we need to through an error
    raise FileNotFoundError(f"{filename} file not found")


def find_allcontributorsrc():
    """Find the full path of the .all-contributorsrc file"""

    return find_file_in_path_list(".all-contributorsrc", allcontributorsrc_path_list())


def find_rolefile(name="roles.yaml"):
    """Find a given role definition file"""

    return find_file_in_path_list(name, rolefile_path_list())


def have_allcontributorsrc():
    try:
        find_allcontributorsrc()
        return True
    except FileNotFoundError:
        return False


def read_allcontributorsrc():
    """Read the allcontributorsrc file and return it as a dictionary"""
    filename = find_allcontributorsrc()

    with open(filename, "r") as rcfile:
        return json.load(rcfile)


def write_allcontributorsrc(data):
    """Write a dictionary into the allcontributorsrc file"""

    if have_allcontributorsrc():
        filename = find_allcontributorsrc()
    else:
        # Use the current working directory as the location of the newly
        # created allcontributorsrc file unless we are in a git repository
        filename = os.path.join(os.getcwd(), ".all-contributorsrc")
        if is_in_git_repository():
            filename = os.path.join(get_repository(), ".all-contributorsrc")

    with open(filename, "w") as rcfile:
        json.dump(data, rcfile, indent=2)


def get_template_loader():
    """Create a Jinja2 Template Loader that takes into account all relevant paths"""

    # Always take into account the current working directory
    loader_list = [jinja2.FileSystemLoader("templates")]

    # Take into account the git directory if we are in a repository
    if is_in_git_repository():
        loader_list.append(
            jinja2.FileSystemLoader(os.path.join(get_repository(), "templates"))
        )

    # Always add the creditall package directory to find the default templates
    loader_list.append(jinja2.PackageLoader("creditall"))

    # The ChoiceLoader class implements the dispatch between individual loaders
    return jinja2.ChoiceLoader(loader_list)
