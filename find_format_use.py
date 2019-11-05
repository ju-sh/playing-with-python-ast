import ast
import argparse
from pprint import pprint

from unparse import Unparser

class FormatExtract(ast.NodeVisitor):
    """
    Class to find location of `str.format()`
    """

    def __init__(self):
        self.line_col_list = []

    def visit_Call(self, node):
        """
        Automatically called when a `Call` object is found
        """

        # Check if `str.format()` is used
        if(isinstance(node.func, ast.Attribute)
           and isinstance(node.func.value, ast.Str)
           and (node.func.attr == 'format')
        ):
            # `node.col_offset` can be used for column number
            self.line_col_list.append(node.lineno)    # append lineno to the list
            print(f"{node.lineno}")
            print(Unparser(node).get_result(), "\n")

        # Consider the children nodes as well
        self.generic_visit(node)
        return node

if __name__ == "__main__":

    # Set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("in_file", nargs='+')   # positional arg
    parser.add_argument("--nl", const=5, type=int, nargs='?')   # optional arg=>if no parameter, val from const will be used
    args = parser.parse_args()

    # Do the work
    input_file_name_list = args.in_file
    for i, input_file_name in enumerate(input_file_name_list):
        print(f"===> {input_file_name} <===")
        try:
            with open(input_file_name) as fin:
                input_file_contents = fin.read()
                module = ast.parse(input_file_contents)
                fmt_extr = FormatExtract()
                fmt_extr.visit(module)
        except FileNotFoundError:
            print(f"Error: file `{input_file_name}` could not be opened. Skipping...")
            continue

        # Remove duplicates in list. Set will make mess up order. So use sorted.
        line_nos = sorted(set(fmt_extr.line_col_list))

        if args.nl:
            # Group the line numbers if `nl` is specified
            nl = args.nl
            ll = [line_nos[i:i+nl] for i in range(0, len(line_nos), nl)]
            pprint(ll)
        else:
            print(line_nos)
# To-do
# -----
# option for showing lines as well
# support string as input??
# use logger
