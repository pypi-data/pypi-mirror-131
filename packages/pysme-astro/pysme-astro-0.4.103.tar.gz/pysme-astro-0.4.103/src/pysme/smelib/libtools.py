# -*- coding: utf-8 -*-
# This file is complementary to cwrapper.py, but since we simply want to
# copy cwrapper from the smelib, this has all the additional methods in it
# that are relevant to PySME but not the smelib
# ATM those are related to the location of the library and its download

import ctypes as ct
import logging
import os
import platform
import subprocess
import zipfile
from os.path import dirname, exists, join
from posixpath import realpath

import wget

logger = logging.getLogger(__name__)


def download_libsme(loc=None):
    if loc is None:
        loc = dirname(dirname(get_full_libfile()))
    # Download compiled library from github releases
    print("Downloading and installing the latest libsme version for this system")
    aliases = {
        "Linux": "manylinux2014_x86_64",
        "Windows": "windows",
        "Darwin": "macos",
    }
    system = platform.system()

    try:
        system = aliases[system]
    except KeyError:
        raise KeyError(
            "Could not find the associated compiled library for this system {}. Either compile it yourself and place it in src/pysme/ or open an issue on Github"
        )

    github_releases_url = "https://github.com/AWehrhahn/SMElib/releases/latest/download"
    github_releases_fname = "{system}-gfortran.zip".format(system=system)
    url = github_releases_url + "/" + github_releases_fname
    fname = join(loc, github_releases_fname)

    if exists(fname):
        os.remove(fname)

    print("Downloading file %s" % url)
    os.makedirs(loc, exist_ok=True)
    wget.download(url, out=loc)

    zipfile.ZipFile(fname).extractall(loc)

    os.remove(fname)


def compile_interface():
    libdir = join(dirname(__file__))
    cwd = os.getcwd()
    os.chdir(libdir)
    subprocess.run(["python", "setup.py", "build_ext", "--inplace"])
    os.chdir(cwd)


def get_lib_name():
    """Get the name of the sme C library"""
    system = platform.system().lower()

    if system == "windows":
        return "libsme-5.dll"

    arch = platform.machine()
    bits = 64  # platform.architecture()[0][:-3]

    return "sme_synth.so.{system}.{arch}.{bits}".format(
        system=system, arch=arch, bits=bits
    )


def get_lib_directory():
    if platform.system() in ["Windows"]:
        dirpath = "bin"
    else:
        # For Linux/MacOS
        dirpath = "lib"
    return dirpath


def get_full_libfile():
    """Get the full path to the sme C library"""
    localdir = dirname(dirname(__file__))
    libfile = get_lib_name()
    dirpath = get_lib_directory()
    libfile = join(localdir, dirpath, libfile)
    return libfile


def load_library(libfile=None):
    if libfile is None:
        libfile = get_full_libfile()
    try:
        os.add_dll_directory(dirname(libfile))
    except AttributeError:
        newpath = dirname(libfile)
        if "PATH" in os.environ:
            newpath += os.pathsep + os.environ["PATH"]
        os.environ["PATH"] = newpath
    return ct.CDLL(str(libfile))


def get_full_datadir():
    localdir = dirname(dirname(__file__))
    datadir = join(localdir, "share/libsme/")
    return datadir
