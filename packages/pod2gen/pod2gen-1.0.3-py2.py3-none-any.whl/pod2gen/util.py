# -*- coding: utf-8 -*-
"""
    pod2gen.util
    ~~~~~~~~~~~~

    This file contains helper functions for the feed generator module.

    :copyright: 2013, Lars Kiesow <lkiesow@uos.de>; 2016, Thorben Dahl
        <thorben@sjostrom.no>; 2021, Slim Beji <mslimbeji@gmail.com>
    :license: FreeBSD and LGPL, see license.* for more details.
"""
import html
import locale


def ensure_format(val, allowed, required, allowed_values=None, defaults=None):
    """Takes a dictionary or a list of dictionaries and check if all keys are in
    the set of allowed keys, if all required keys are present and if the values
    of a specific key are ok.

    :param val:            Dictionaries to check.
    :param allowed:        Set of allowed keys.
    :param required:       Set of required keys.
    :param allowed_values: Dictionary with keys and sets of their allowed values.
    :param defaults:       Dictionary with default values.
    :returns:              List of checked dictionaries.
    """
    # TODO: Check if this function is obsolete and perhaps remove it
    if not val:
        return None
    if allowed_values is None:
        allowed_values = {}
    if defaults is None:
        defaults = {}
    # Make shure that we have a list of dicts. Even if there is only one.
    if not isinstance(val, list):
        val = [val]
    for elem in val:
        if not isinstance(elem, dict):
            raise ValueError("Invalid data (value is no dictionary)")
        # Set default values

        for k, v in defaults.items():
            elem[k] = elem.get(k, v)
        if not set(elem.keys()) <= allowed:
            raise ValueError("Data contains invalid keys")
        if not set(elem.keys()) >= required:
            raise ValueError("Data contains not all required keys")

        for k, v in values.items():
            if elem.get(k) and not elem[k] in v:
                raise ValueError("Invalid value for %s" % k)
    return val


def formatRFC2822(d):
    """Format a datetime according to RFC2822.

    This implementation exists as a workaround to ensure that the locale setting
    does not interfere with the time format. For example, day names might get
    translated to your local language, which would break with the standard.

    :param d: Time and date you want to format according to RFC2822.
    :type d: datetime.datetime
    :returns: The datetime formatted according to the RFC2822.
    :rtype: str
    """
    l = locale.setlocale(locale.LC_ALL)
    locale.setlocale(locale.LC_ALL, "C")
    d = d.strftime("%a, %d %b %Y %H:%M:%S %z")
    locale.setlocale(locale.LC_ALL, l)
    return d


def htmlencode(s):
    """Encode the given string so its content won't be confused as HTML
    markup.
    """
    return html.escape(s)


def listToHumanreadableStr(l):
    """Create a human-readable string out of the given iterable.

    Example::

        >>> from pod2gen.util import listToHumanreadableStr
        >>> listToHumanreadableStr([1, 2, 3])
        1, 2 and 3

    The string ``(empty)`` is returned if the list is empty – it is assumed
    that you check whether the list is empty yourself.
    """
    # TODO: Allow translations of "and" and "empty"
    length = len(l)
    l = [str(e) for e in l]

    if length == 0:
        return "(empty)"
    elif length == 1:
        return l[0]
    else:
        return ", ".join(l[:-1]) + " and " + l[-1]
