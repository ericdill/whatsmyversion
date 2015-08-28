import subprocess
import os
import logging

logger = logging.getLogger(__name__)

git_describe_cmd = ['git', 'describe', '--dirty', '--long', '--always', '--tags']

# need to convert this into a validating regex
pep440 = r'[N!]N(.N)*[{a|b|rc}N][.postN][.devN]'

def git_describe(git_root, version_prefix, version_suffix, use_local_version_id=False):
    desc = subprocess.check_output(git_describe_cmd, cwd=git_root).strip()
    if isinstance(desc, bytes):
        desc = desc.decode('utf8')
    # get the partial git hash. This will inform us which part of the git describe is
    # part of the 'local version identifier'
    full_hash = subprocess.check_output(['git', "rev-parse", "HEAD"],
                                        cwd=git_root).decode()
    partial_hash = full_hash[:7]
    split_desc = desc.split('-')
    logger.info('split_desc = %s' % split_desc)

    dirty = ''
    # man this is going to be a terrible bug when the first six characters of
    # the git hash contain `dirty`
    if 'dirty' in split_desc[-1]:
        dirty = split_desc.pop(-1)

    prefix, suffix, local_id = split_desc

    # add the prefix if you didn't tag it like you wanted it
    if not prefix.startswith(version_prefix):
        prefix = version_prefix + prefix

    # if there have been commits to the repo since the tag, then add the
    # suffix, otherwise do not
    if int(suffix) > 0:
        version = prefix + version_suffix + suffix
    else:
        version = prefix
    # add the local identifier (the first bit of the git hash) to the version
    if use_local_version_id:
        # PEP440 formatting of the local identifier
        version += '+' + local_id
    if dirty:
        # if you're building from uncommitted repos, shame on you...
        version += '+' + dirty

    return version


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
    # logger.info('path = %s' % path)
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
        version.replace('_', '+')
        return version


def version(python_module_path, version_prefix='', version_suffix='.post',
            use_local_version_id=True):
    """Generate a version string for the given python module

    Parameters
    ----------
    python_module_path : str
        Path to the python module for which you want a version
    version_prefix : str, optional
        The prefix for the entire version string
    version_suffix : {a, b, rc, .post, .dev}
        The string to insert between the [major.minor.micro] versions and the
        number of commits since that release
    use_local_version_id : bool, optional
        This will be formatted like this: +[git_hash][-dirty]
        where git_hash is the first 6 characters of the git hasn
              dirty is a flag that signifies that the python source has
              uncommitted information
    """
    try:
        git_path = find_git_root(python_module_path)
        return git_describe(git_path, version_prefix, version_suffix,
                            use_local_version_id)
    except NotAGitRepoError:
        logger.info("The module located at %s does not have a git repo in "
                    "its directory hierarchy" % python_module_path)
        pass

    return version_in_folder_name(python_module_path)

version_metadata = {
    'version_prefix': 'v',
    'version_suffix': '.post',
}

__version__ = version(__file__, **version_metadata)
