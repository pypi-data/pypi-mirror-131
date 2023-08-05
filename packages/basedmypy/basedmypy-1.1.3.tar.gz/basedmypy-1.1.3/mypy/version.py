import os
from mypy import git

# Base version.
# - Release versions have the form "0.NNN".
# - Dev versions have the form "0.NNN+dev" (PLUS sign to conform to PEP 440).
# - For 1.0 we'll switch back to 1.2.3 form.
__version__ = '1.1.3'
base_version = __version__
mypy_version = "0.920 (4d2ff58e)"

mypy_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
if __version__.endswith('+dev') and git.is_git_repo(mypy_dir) and git.have_git():
    __version__ += '.' + git.git_revision(mypy_dir).decode('utf-8')
    mypy_version += '.' + git.git_revision(mypy_dir).decode('utf-8')
    if git.is_dirty(mypy_dir):
        __version__ += '.dirty'
        mypy_version += '.dirty'
del mypy_dir
