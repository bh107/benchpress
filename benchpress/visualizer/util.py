# -*- coding: utf-8 -*-

import argparse


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
        '--labels-to-display',
        metavar="RegEx",
        default=".*",
        help="All stacks that match the RegEx are showed in the generated graph(s)."
    )
    parser.add_argument(
        '--labels-not-to-display',
        metavar="RegEx",
        default="NotIncluded",
        help="All stacks that match the RegEx are not showed in the generated graph(s)."
    )
    parser.add_argument(
        '--label-map',
        default=None,
        metavar="RegEx:label,...,RegEx:label",
        help="Comma separated list of original-to-new-stack names"
    )
    return parser
