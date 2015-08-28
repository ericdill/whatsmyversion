import subprocess
import os
import logging

logger = logging.getLogger(__name__)

git_describe_cmd = ['git', 'describe', '--dirty', '--long', '--always', '--tags']


def git_describe(git_root):
    """Given a path known to contain a .git folder, return a version

    Parameters
    ----------
    package_dir : str
        Absolute path to the root of the package
    """
    print('git_root = %s' % git_root)
    desc = subprocess.check_output(git_describe_cmd, cwd=git_root).strip()
    if isinstance(desc, bytes):
        desc = desc.decode('utf8')
    return desc

class NotAGitRepoError(RuntimeError):
    pass

def find_git_root(path):
    """Recursively search up the path hierarchy for the git folder

    Parameters
    ----------
    path : str
        Path to start looking for a .git folder

    Returns
    -------
    str :
        Path to the git folder. Raises exception if no .git folder is found
    """
    # print('path = %s' % path)
    if path == os.sep:
        raise NotAGitRepoError()

    if os.path.isdir(path) and '.git' in os.listdir(path):
        return path
    return find_git_root(os.path.dirname(path))


def version_in_folder_name(path):
    """Assume that the file comes from a `python setup.py install`

    Parameters
    ----------
    path : str
        Path to the module in the project for which you want to know the version

    Returns
    -------
    str :
        The version string according to the folder
    """
    if 'site-packages' in path:
        # this file was installed via python setup.py install. The version is
        # the thing that comes after the 'site-packages' folder
        split_path = path.split(os.sep)
        version_info_folder = split_path[split_path.index('site-packages')+1]
        logger.debug('version_info_folder = %s' % version_info_folder)
        split_version_info = version_info_folder.split('-')
        logger.debug('split_version_info = %s' % split_version_info)
        package_name = split_version_info[0]
        idx = len(split_version_info) - 1
        while 'egg' not in split_version_info[idx]:
            idx -= 1
        version = split_version_info[1:idx]
        if len(version) > 1:
            raise RuntimeError("It is not clear why the version string is not "
                               "a one-element list at this point = %s" % version)
        version = version[0]
        return version


def version(python_module_path):
    try:
        git_path = find_git_root(python_module_path)
        return git_describe(git_path)
    except NotAGitRepoError:
        logger.info("The module located at %s does not have a git repo in "
                    "its directory hierarchy" % python_module_path)
        pass

    return version_in_folder_name(python_module_path)

__version__ = version(__file__)
