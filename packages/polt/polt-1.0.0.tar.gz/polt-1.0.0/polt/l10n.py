# system modules
import locale
import itertools
import gettext
import os
import sys
import ctypes
from pkg_resources import resource_filename

# internal modules

# external modules


GETTEXT_DOMAIN = "polt"
LOCALEDIR = resource_filename("polt", "locale")

# set up localization
locale.setlocale(locale.LC_ALL, "")

# taken from https://stackoverflow.com/a/42577134
try:
    if hasattr(locale, "bindtextdomain"):
        libintl = locale
    elif os.name == "nt":
        libintl = ctypes.cdll.LoadLibrary("libintl-8.dll")
    elif sys.platform == "darwin":
        libintl = ctypes.cdll.LoadLibrary("libintl.dylib")

    libintl.bindtextdomain(GETTEXT_DOMAIN, LOCALEDIR)

except (OSError, AttributeError):
    pass

gettext.bindtextdomain(GETTEXT_DOMAIN)
gettext.textdomain(GETTEXT_DOMAIN)
gettext.install(GETTEXT_DOMAIN, localedir=LOCALEDIR)


def join(strings, sep=", ", last_sep=" {} ".format(_("and"))):
    """
    Joins a sequence of strings with a separator and use another separator for
    the last one.

    Args:
        strings (iterable of str): the strings to join
        sep (str, optional): the separator to use except for the last element
        last_sep (str, optional): the separator to use for the last element

    Returns:
        str : the joined string
    """
    strings = list(strings)
    if not strings:
        return ""
    if len(strings) > 1:
        return last_sep.join((sep.join(strings[:-1]), strings[-1]))
    else:
        return next(iter(strings), str(strings))
