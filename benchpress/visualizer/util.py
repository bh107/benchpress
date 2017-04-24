# -*- coding: utf-8 -*-

import argparse
import re


def filter_cmd_list(cmd_list, regex_to_include=".*", regex_to_exclude=None, dict_key='label'):
    """Filter a list of Benchpress commands

    Parameters
    ----------
    cmd_list : list of dict
        The commands to filter.
    regex_to_include : str
        RegEx that match for inclusion.
    regex_to_exclude : str
        RegEx that match for exclusion.
    dict_key : str
        The dict-key in the command to search within.

    Returns
    -------
    new_cmd_list : list of dict
        New list of commands.
    """
    ret = []
    for cmd in cmd_list:
        if re.search(regex_to_include, cmd[dict_key]) is not None:
            if regex_to_exclude is None or re.search(regex_to_exclude, cmd[dict_key]) is None:
                ret.append(cmd.copy())
    return ret


def translate_dict(cmd_list, label_map, dict_key='label'):
    """Create a translate dictionary of labels
    
    Parameters
    ----------
    cmd_list : list of dict
        The Benchpress commands to translate
    label_map : dict
        Dictionary mapping old to new labels: {'old_label': 'new_label'}. 
    dict_key
        The dict-key in the command to translate. 

    Returns
    -------
    new_cmd_list : list of dict 
        Copy of `cmd_list` sorted in the same order as `label_map`
    dictionary : dict
        Dictionary mapping old to new labels of ALL commands in 'cmd_list'
    """
    cmd_list = list(cmd_list)  # We need a copy since we pop items as we go
    ret_map = {}
    ret_list = []
    if label_map is not None:
        for (old, new) in label_map:
            if len(new) > 0:
                for i in range(len(cmd_list)):
                    if re.search(old, cmd_list[i][dict_key]) is not None:
                        ret_map[cmd_list[i][dict_key]] = new
                        ret_list.append(cmd_list[i])
                        cmd_list.pop(i)
                        break
    for old, new in [(t, t) for t in cmd_list]:
        ret_map[old[dict_key]] = new[dict_key]
        ret_list.append(old)
    return ret_list, ret_map


def default_argparse(description):
    """Get the default argparse object
    
    Call .parse_args() on the returned object to get the arguments 
    
    Parameters
    ----------
    description : str
        ArgumentParser description
    
    Returns
    -------
    parser : argparse.ArgumentParser
        The parser object       
    """
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("results", help="JSON file containing results")
    parser.add_argument(
        "--regex",
        type=str,
        default='elapsed-time: ([\d.]+)',
        help="How to parse the result of each run. The RegEX should contain exactly one group."
    )
    parser.add_argument(
        "--py_type",
        choices=['float', 'int', 'str'],
        default='float',
        # Convert the choice represented as a string to a Python type object e.g. "float" => float
        type=lambda x: eval(x),
        help="The Python data type of the parsed results."
    )
    parser.add_argument(
        '--labels-to-include',
        metavar="RegEx",
        type=str,
        default=".*",
        help="All labels that match the RegEx are showed."
    )
    parser.add_argument(
        '--labels-to-exclude',
        metavar="RegEx",
        type=str,
        default=None,
        help="All labels that match the RegEx are ignored."
    )

    def label_map2tuple(string):
        """Convert "RegEx:label,...,RegEx:label" => [("RegEx","label"),...,("RegEx","label")]"""
        ret = []
        for tok in string.split(","):
            if ":" not in tok:
                raise argparse.ArgumentError()
            (old, new) = tok.split(":")
            ret.append((old, new))
        return ret
    parser.add_argument(
        '--label-map',
        default=None,
        type=label_map2tuple,
        metavar="RegEx:label,...,RegEx:label",
        help="Comma separated list of original-to-new-label names"
    )
    return parser
