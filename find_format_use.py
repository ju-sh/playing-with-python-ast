import ast
import argparse
from pprint import pprint

class FormatExtract(ast.NodeVisitor):
    def __init__(self):
        self.line_col_list = []

    def visit_Call(self, node):
        self.generic_visit(node)
        if(isinstance(node.func, ast.Attribute)
           and isinstance(node.func.value, ast.Str)
           and (node.func.attr == 'format')
        ):
            # `node.col_offset` can be used for column number
            self.line_col_list.append(node.lineno)    # append lineno to the list
        self.generic_visit(node)    # To consider the children nodes as well
        return node

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("in_file", nargs='+')   # positional arg
    parser.add_argument("--nl", const=5, type=int, nargs='?')   # optional arg=>if no parameter, val from const will be used
    args = parser.parse_args()
    
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
