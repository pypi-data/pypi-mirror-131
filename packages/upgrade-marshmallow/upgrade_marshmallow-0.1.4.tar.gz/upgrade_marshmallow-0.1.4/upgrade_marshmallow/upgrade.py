"""Upgrade Assembly"""

import ast
import typing as T
from collections import defaultdict

import astor

ARG = T.TypeVar('ARG')  # TODO: bind str
VALUE = T.TypeVar('VALUE')  # TODO: bind Any
PATH = T.TypeVar('PATH')  # TODO: bind str

RENAME_ARGUMENTS: dict = {
    'default': 'dump_default',
    'missing': 'load_default',
}

_FIELD_ARGUMENTS: list = [
    # 'default',
    # 'missing',
    'data_key',
    'attribute',
    'validate',
    'required',
    'allow_none',
    'load_only',
    'dump_only',
    'error_messages',
    'metadata'
]

__fields_args = _FIELD_ARGUMENTS.copy()
__fields_args.extend(RENAME_ARGUMENTS.keys())
__fields_args.extend(RENAME_ARGUMENTS.values())

field_arguments = set(__fields_args)


MAPPING = {}
TREE = defaultdict(dict)


def replace_as_metadata_kw(
    file: PATH,
    *,
    indent: int = 4,
):
    """
    Args:
        - file (str): source code file path
        - indent (int): indent of source code
    """
    tree = astor.parse_file(file)

    find_rename_fields = FindRenameFields()
    find_rename_ma = FindRenameMarshmallow()
    find_imported_into_field = FindImportedIntoField()

    # Replace metadata -------------------------------------------------------

    rpl_metadata = ReplaceAsMetadataKW()
    rpl_metadata_id = id(rpl_metadata)

    MAPPING[id(find_rename_fields)] = rpl_metadata_id
    MAPPING[id(find_rename_ma)] = rpl_metadata_id
    MAPPING[id(find_imported_into_field)] = rpl_metadata_id

    TREE[rpl_metadata_id]['fields'] = 'fields'
    TREE[rpl_metadata_id]['marshmallow'] = 'marshmallow'
    TREE[rpl_metadata_id]['imported_fields'] = set()

    find_rename_fields.visit(tree)
    find_rename_ma.visit(tree)
    find_imported_into_field.visit(tree)
    tree = rpl_metadata.visit(tree)

    # Replace default->dump_default, missing->load_default -------------------

    rpl_default_missing = ReplaceDefaultAndMissing()
    rpl_default_missing_id = id(rpl_default_missing)

    MAPPING[id(find_rename_fields)] = rpl_default_missing_id
    MAPPING[id(find_rename_ma)] = rpl_default_missing_id
    MAPPING[id(find_imported_into_field)] = rpl_default_missing_id

    TREE[rpl_default_missing_id]['fields'] = 'fields'
    TREE[rpl_default_missing_id]['marshmallow'] = 'marshmallow'
    TREE[rpl_default_missing_id]['imported_fields'] = set()

    find_rename_fields.visit(tree)
    find_rename_ma.visit(tree)
    find_imported_into_field.visit(tree)
    new_tree = rpl_default_missing.visit(tree)

    ast.fix_missing_locations(new_tree)

    # TODO: formatter + comment issue
    #   - formatter: yapf + --style='{based_on_style: pep8, indent_width: 2}'
    #   - comment: no solution yet
    codes = astor.to_source(new_tree, indent_with=' ' * indent)
    return codes


class FindRenameFields(ast.NodeTransformer):
    def visit_ImportFrom(self, node: ast.ImportFrom) -> T.Any:
        node_transformer_id = MAPPING[id(self)]

        if node.module == 'marshmallow':
            for alias in node.names:
                if alias.name == 'fields':
                    # case: `from marshmallow import fields as ma_fields`
                    TREE[node_transformer_id]['fields'] = alias.asname or alias.name

        return node


class FindRenameMarshmallow(ast.NodeTransformer):
    def visit_Import(self, node: ast.Import) -> T.Any:
        node_transformer_id = MAPPING[id(self)]

        for alias in node.names:
            if alias.name == 'marshmallow':
                # case: `import marshmallow as ma`
                TREE[node_transformer_id]['marshmallow'] = alias.asname or alias.name

        return node


class FindImportedIntoField(ast.NodeTransformer):
    def visit_ImportFrom(self, node: ast.ImportFrom) -> T.Any:
        node_transformer_id = MAPPING[id(self)]
        if node.module.endswith('marshmallow.fields'):
            for alias in node.names:
                TREE[node_transformer_id]['imported_fields'].add(alias.asname or alias.name)
        return node


def is_marshmallow_feild_call_expression(node: ast.Call, rpl_obj_id: int) -> bool:
    # case:
    #   from marshmallow import fields
    #   class FooSchema(Schema):
    #       foo = fields.String(title='foo', description='foo')
    #                   ^
    if isinstance(node.func, ast.Attribute):
        attr: ast.Attribute = node.func

        # case: `marshmallow.fields.String()`
        # Call(func=Attribute(value=Attribute(value=Name(id='marshmallow', ctx=), attr='fields', ctx=), attr='String', ctx=), args=[], keywords=[
        # ^         ^               ^               ^                                   ^                           ^
        # node     node.func       node.func.value node.func.value.value               node.func.value.attr         node.func.attr
        #
        if isinstance(attr.value, ast.Attribute):
            if isinstance(attr.value.value, ast.Name):
                if attr.value.value.id == TREE[rpl_obj_id]['marshmallow']:
                    if attr.value.attr == 'fields':
                        return True

        # foo = fields.String(title='foo', description='foo')
        #       ^
        if isinstance(attr.value, ast.Name):
            if node.func.value.id == TREE[rpl_obj_id]['fields']:
                return True
            # Just others ast.Call, but not rely to marshmallow.fields
            else:
                pass
    # case: `from marshmallow.fields import String`
    elif (isinstance(node.func, ast.Name)
          and node.func.id in TREE[rpl_obj_id]['imported_fields']):
        return True

    # Just others ast.Call, but not rely to marshmallow.fields
    else:
        pass
    return False


class ReplaceAsMetadataKW(ast.NodeTransformer):
    def visit_Call(self, node: ast.Call) -> T.Any:
        if not is_marshmallow_feild_call_expression(node, id(self)):
            return node

        kws = node.keywords[:]
        node.keywords.clear()
        metadata: T.List[T.Tuple[ARG, VALUE]] = []
        for kw_obj in kws:
            # metadata
            if kw_obj.arg not in field_arguments:
                metadata.append((kw_obj.arg, kw_obj.value))
            # the sig.parameters
            else:
                node.keywords.append(kw_obj)

        for kw_obj in node.keywords:
            # TODO: fields.String(required=True, title='name', metadata={'description': '...'})
            if kw_obj.arg == 'metadata':
                raise RuntimeError('not handle ths condition!')

        if metadata:
            node.keywords.append(ast.keyword(
                arg='metadata',
                value=ast.Dict(
                    keys=[ast.Constant(value=arg, kind=None)
                        for arg, _ in metadata],
                    values= [value for _, value in metadata]
                    )
            ))
        return node


class ReplaceDefaultAndMissing(ast.NodeTransformer):
    def visit_Call(self, node: ast.Call) -> T.Any:
        if not is_marshmallow_feild_call_expression(node, id(self)):
            return node

        kws = node.keywords[:]
        node.keywords.clear()
        # rename = []
        for kw_obj in kws:
            if kw_obj.arg in RENAME_ARGUMENTS:
                # rename.append()
                node.keywords.append(ast.keyword(
                    arg=RENAME_ARGUMENTS[kw_obj.arg],
                    value=kw_obj.value
                ))
            else:
                node.keywords.append(kw_obj)

        return node
