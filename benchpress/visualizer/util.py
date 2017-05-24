# -*- coding: utf-8 -*-
from __future__ import absolute_import
import argparse
import re
import math
import json


class Color:
    HEAD = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'


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


def mean(values):
    """Calculate the mean.
    
    Parameters
    ----------
    values : list
        Values to find the mean of
        
    Returns
    -------
    out : float
        The mean
    """
    return sum(values)/float(len(values)) if len(values) > 0 else 0.0


def variance(values):
    """Calculate the variance.

    Parameters
    ----------
    values : list
        Values to find the variance of

    Returns
    -------
    out : float
        The variance
    """
    count = len(values)
    if count < 2:
        return 0.0
    x_avg = mean(values)
    return mean([abs(x - x_avg)**2 for x in values])


def standard_deviation(values):
    """Calculate the standard deviation.

    Parameters
    ----------
    values : list
        Values to find the standard deviation of

    Returns
    -------
    out : float
        The standard deviation
    """
    count = len(values)
    if count < 2:
        return 0.0
    x_avg = mean(values)
    return math.sqrt(mean([abs(x - x_avg)**2 for x in values]))


def extract_succeed_results(cmd, regex, py_type=int, dict_key='stdout'):
    """Extract the values of the succeed results
    
    Parameters
    ----------
    cmd : dict
        The Benchpress command to extract from
    regex : str
        The regex that extract a value from each result
    py_type : type
        The Python type of the extracted 
    dict_key : str
        The dictionary key to extract from

    Returns
    -------
    values : list
        List of extracted values
    """
    ret = []
    for job in cmd.get('jobs', []):
        for res in job.get('results', []):
            match_list = re.findall(regex, res[dict_key])
            if res['success'] and len(match_list) > 0:
                for match in match_list:
                    ret.append(py_type(match))
    return ret


def default_argparse(description, multiple_result_files=False):
    """Get the default argparse object
    
    Call .parse_args() on the returned object to get the arguments 
    
    Parameters
    ----------
    description : str
        ArgumentParser description
        
    multiple_result_files : bool
        When True, the `results` arg is a list of suite files
    
    Returns
    -------
    parser : argparse.ArgumentParser
        The parser object       
    """
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    if multiple_result_files:
        parser.add_argument(
            "results",
            metavar="FILE_LIST",
            type=argparse.FileType('r'),
            nargs='+',
            help="JSON file containing results (accept multiple files)"
        )
    else:
        parser.add_argument(
            "results",
            metavar="FILE",
            type=argparse.FileType('r'),
            help="JSON file containing results"
        )
    parser.add_argument(
        "-o", "--output",
        type=argparse.FileType('w'),
        default=None,
        metavar="FILE",
        help="Write output to FILE."
    )
    parser.add_argument(
        "--parse-regex",
        metavar="RegEx",
        type=str,
        default='elapsed-time: ([\d.]+)',
        help="How to parse the result of each run. For each RegEx match, group one is recorded as a result."
    )
    parser.add_argument(
        "--py-type",
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

    def label_map2tuple(arg_str):
        """Convert "RegEx:label,...,RegEx:label" => [("RegEx","label"),...,("RegEx","label")]"""
        ret = []
        for tok in arg_str.split(","):
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


def texsafe(text):
    """Escape text such that it is tex-safe."""
    conv = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless',
        '>': r'\textgreater',
    }
    escaped = []

    for char in text:
        if char in conv:
            char = conv[char]
        escaped.append(char)
    return "".join(escaped)


def means_series_map(args):
    """Create a dict that map a command label and meta-key to a pair of mean and standard deviation

    Such as means['Bean']['2017-05-02 13:29:34.87'] = (0.1289, 0.0006)

    Parameters
    ----------
    args : argparse.Namespace
        The parsed argparse object to build the map from.

    Returns
    -------
    means : dict
        The dict that maps command label and date to a pair of mean and standard deviation
    cmd_labels : list
        List of commands labels found in `args`
    meta-keys : list
        List of meta key values found in `args`
    """
    # First we create `means` which map a command label and date to a pair of mean and standard deviation
    # e.g. means['Bean']['2017-05-02 13:29:34.87'] = (0.1289, 0.0006)
    means = {}
    cmd_labels = set()
    meta_keys = set()
    for result in args.results:
        suite = json.load(result)
        meta_key = suite[args.meta_key]
        cmd_list = suite['cmd_list']
        cmd_list = filter_cmd_list(cmd_list, args.labels_to_include, args.labels_to_exclude)
        for cmd in cmd_list:
            succeed_values = extract_succeed_results(cmd, args.parse_regex, args.py_type)
            avg = mean(succeed_values)
            std = standard_deviation(succeed_values)
            if cmd['label'] not in means:
                means[cmd['label']] = {}
            means[cmd['label']][meta_key] = (avg, std)
            cmd_labels.add(cmd['label'])
            meta_keys.add(meta_key)
    return (means, sorted(list(cmd_labels)), sorted(list(meta_keys)))
