#!/usr/bin/env python
"""
Some imports to make sure that the DIRACOS environment is complete
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import traceback
import warnings
import pytest

parametrize = pytest.mark.parametrize


# This list was obtained by checking all the imports in DIRAC v6r20
# Since the parsing was not precise, the list might not be exhaustive, but well...
# The starting point was these two searches
#  find . -name '*.py' -exec grep '^import ' {} \; | grep -v DIRAC | grep -v ' as ' |  sort -u
# find . -name '*.py' -exec grep '^from ' {} \; | grep -v DIRAC | awk
# {'print $2'} | sort -u | grep -v '\.'

# Notes that these scripts will make some false positive appear
# As of now, they are
# config
# diracdoctools
# diracdoctools.cmd
# dont_import_two
# local_stuff
# modules_in_one_line
# more_local_stuff
# some_third_party_lib
# some_third_party_other_lib


moduleNames = [
    "arc",
    "argparse",
    "array",
    "ast",
    "atexit",
    "base64",
    "binascii",
    "builtins",
    "bz2",
    "calendar",
    "certifi",
    "cgi",
    "cmd",
    "collections",
    "contextlib",
    "copy",
    "csv",
    "datetime",
    "difflib",
    "distutils.spawn",
    "elasticsearch",
    "elasticsearch_dsl",
    "errno",
    "fcntl",
    "filecmp",
    "fnmatch",
    "fts3",
    "functools",
    "__future__",
    "getopt",
    "getpass",
    "gfal2",
    "git",
    "glob",
    "gzip",
    "hashlib",
    "http.client",
    "hypothesis",
    "imp",
    "importlib",
    "inspect",
    "io",
    "itertools",
    "json",
    "logging",
    "lz4",
    "M2Crypto",
    "math",
    "matplotlib",
    "mock",
    "multiprocessing",
    "MySQLdb",
    "numpy",
    "operator",
    "optparse",
    "os",
    "os.path",
    "pickle",
    "pkgutil",
    "platform",
    "pprint",
    "psutil",
    "pwd",
    "pyasn1_modules",
    "pylab",
    "pyparsing",
    "pytest",
    "pytz",
    "pyxrootd.client",
    "random",
    "re",
    "readline",
    "requests",
    "resource",
    "select",
    "setuptools",
    "shlex",
    "shutil",
    "signal",
    "six",
    "smtplib",
    "socket",
    "sqlalchemy",
    "sqlite3",
    "ssl",
    "stat",
    "stomp",
    "string",
    "_strptime",
    "struct",
    "subprocess",
    "subprocess32",
    "suds",
    "sys",
    "syslog",
    "tarfile",
    "tempfile",
    "textwrap",
    "_thread",
    "threading",
    "time",
    "traceback",
    "types",
    "unittest",
    "urllib",
    "xml.dom.minidom",
    "xml.sax",
    "xxhash",
    "zipfile",
    "zlib",
]

# List here the modules that are allowed to Fail.
# Ideally, this should always be empty...
ALLOWED_TO_FAIL = []

# List of modules that need graphic libraries.
# When failing, these tests are just marked as skipped with a warning
GRAPHIC_MODULES = [
    "pylab",
]

diracosPath = os.path.normpath(os.environ["DIRACOS"])


@parametrize("moduleName", moduleNames)
def test_module(moduleName):
    """Try to import a module and check whether it is located in DIRACOS.

    Modules that are in the ALLOWED_TO_FAIL list are shown as skipped and generate a warning

    Modules that require graphic libraries on the system (GRAPHIC_MODULES) are skipped on container
    """

    try:
        module = __import__(moduleName)

        # Test whether it is correctly imported from DIRACOS

        try:
            modulePath = module.__file__
            # return true, if the common prefix of both is equal to directory
            # e.g. /a/b/c/d.rst and directory is /a/b, the common prefix is /a/b
            assert (
                os.path.commonprefix([modulePath, diracosPath]) == diracosPath
            ), "ERROR %s not from DIRACOS: %s" % (moduleName, modulePath)

        # builtin modules like sys have no path
        except AttributeError as e:
            print("WARNING no path for", moduleName)

    except ImportError as e:
        msg = "could not import %s: %s" % (moduleName, repr(e))
        print(traceback.print_exc())

        if moduleName in ALLOWED_TO_FAIL:
            warnings.warn(msg)
            pytest.skip("WARN: " + msg)
        elif moduleName in GRAPHIC_MODULES:
            warnings.warn(
                msg + "(Possibly due to system graphic libraries not present)"
            )
            pytest.skip(
                "WARN: "
                + msg
                + "(Possibly due to system graphic libraries not present)"
            )
        else:
            pytest.fail("ERROR: " + msg)


def test_gfal_plugins():
    import gfal2

    ctx = gfal2.creat_context()
    plugins = ctx.get_plugin_names()
    print(plugins)
    plugins = dict(x.split("-", 1) for x in plugins)
    assert "dcap" in plugins
    assert "file" in plugins
    assert "gridftp" in plugins
    assert "http" in plugins
    assert "sftp" in plugins
    assert "srm" in plugins
    assert "xrootd" in plugins
