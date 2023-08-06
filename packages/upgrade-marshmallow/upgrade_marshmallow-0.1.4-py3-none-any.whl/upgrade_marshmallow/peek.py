import ast
from collections import defaultdict
from pprint import pp

import astor
from upgrade_marshmallow.astpp import parseprint


def get_svr_methods(filepath):
    tree = astor.parse_file(filepath)
    svr_methods = defaultdict(list)

    class TrackClassMethod(ast.NodeTransformer):
        def visit_ClassDef(self, node):  # noqa: N802
            class_name = node.name
            for sub_node in node.body:
                if isinstance(sub_node, ast.FunctionDef):
                    svr_methods[class_name].append(sub_node.name)
            return node

    TrackClassMethod().visit(tree)
    return svr_methods


import click

@click.command()
@click.argument('file')
def main(file):
    # pp(get_svr_attributes(file))
    with open(file, 'r') as fp:
        codes = fp.read()
        parseprint(codes)


if __name__ == '__main__':
    """
    Usage: python -m upgrade_marshmallow.peek [OPTIONS] FILE
        $ python -m upgrade_marshmallow.peek examples/simple/old_version.py
    """

    main()
