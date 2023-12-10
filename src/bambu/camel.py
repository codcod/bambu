"""
Inspired by:
https://github.com/smeggingsmegger/PyBambooHR/blob/master/PyBambooHR/utils.py
"""
import re


def ctou(word: str) -> str:
    """
    Convert a string from camel case to underscore.
    """
    return re.sub(
        '([a-z0-9])([A-Z])', r'\1_\2', re.sub('(.)([A-Z][a-z]+)', r'\1_\2', word)
    ).lower()


def utoc(word: str) -> str:
    """
    Convert a string from underscore to camel case.
    """
    return re.sub(r'_([a-z])', lambda m: (m.group(1).upper()), word)


def camelcase_keys(src: dict) -> dict:
    """
    Convert keys in a dict to camel case.
    """
    dest = {}
    for key in src:
        if isinstance(src[key], dict):
            dest[utoc(key)] = camelcase_keys(src[key])
        else:
            dest[utoc(key)] = src[key]

    return dest


def underscore_keys(src: dict) -> dict:
    """
    Convert keys in a dict to camel case.
    """
    dest = {}
    for key in src:
        if isinstance(src[key], dict):
            dest[ctou(key)] = underscore_keys(src[key])
        else:
            dest[ctou(key)] = src[key]

    return dest
